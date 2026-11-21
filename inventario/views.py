from datetime import timedelta
from decimal import Decimal
from difflib import SequenceMatcher
from pathlib import Path
import re
import unicodedata
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models import Count, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from .forms import VehiculoForm, VentaForm
from .models import Fotografia, Marca, Modelo, Vehiculo, Venta


def admin_requerido(view):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="acceso",
    )(view)


def inicio(request):
    vehiculos = Vehiculo.objects.filter(estado="Disponible").select_related(
        "modelo", "modelo__marca"
    ).prefetch_related("fotografia_set")
    tipo = request.GET.get("tipo", "")
    if tipo:
        vehiculos = vehiculos.filter(tipo=tipo)

    filtros = {
        "marca": "modelo__marca__nombre__iexact",
        "modelo": "modelo__nombre__icontains",
        "combustible": "combustible__iexact",
        "transmision": "transmision__iexact",
        "precio_min": "precio__gte",
        "precio_max": "precio__lte",
        "anio_min": "anio__gte",
        "anio_max": "anio__lte",
    }
    for name, lookup in filtros.items():
        value = request.GET.get(name, "").strip()
        if value and (not name.startswith(("precio", "anio")) or value.isdigit()):
            vehiculos = vehiculos.filter(**{lookup: value})

    query = request.GET.get("q", "").strip()
    if query:
        direct_matches = vehiculos.filter(
            Q(modelo__nombre__icontains=query)
            | Q(modelo__marca__nombre__icontains=query)
        )
        has_direct_matches = direct_matches.exists()
        candidates = list(direct_matches if has_direct_matches else vehiculos)
        ranked = [(_puntuar_titulo(query, vehicle), vehicle) for vehicle in candidates]
        ranked.sort(key=lambda item: item[0], reverse=True)
        vehiculos = [
            vehicle
            for score, vehicle in ranked
            if has_direct_matches or score >= 0.45
        ]
        if not has_direct_matches:
            vehiculos = vehiculos[:20]

    vehiculos = list(vehiculos)
    secciones = (
        {"id": "automoviles", "nombre": "Carros", "tipos": ("Automóvil",)},
        {
            "id": "camionetas",
            "nombre": "Camionetas y SUV",
            "tipos": ("Camioneta", "SUV", "Pickup"),
        },
        {"id": "camiones", "nombre": "Camiones", "tipos": ("Camión",)},
    )
    grupos_vehiculos = [
        {
            **seccion,
            "vehiculos": [
                vehiculo for vehiculo in vehiculos
                if vehiculo.tipo in seccion["tipos"]
            ],
        }
        for seccion in secciones
    ]

    return render(request, "inventario/inicio.html", {
        "vehiculos": vehiculos,
        "grupos_vehiculos": grupos_vehiculos,
        "tipo_seleccionado": tipo,
        "tipo_choices": Vehiculo.TIPOS,
        "query": query,
        "marcas": Marca.objects.order_by("nombre"),
        "valores_filtro": request.GET,
    })


def _normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(char for char in texto if unicodedata.category(char) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", texto).strip()


def _puntuar_titulo(query, vehicle):
    normalized_query = _normalizar(query)
    title = _normalizar(f"{vehicle.modelo.marca.nombre} {vehicle.modelo.nombre}")
    title_words = title.split()
    query_words = normalized_query.split()
    token_score = sum(
        max(
            (SequenceMatcher(None, word, title_word).ratio() for title_word in title_words),
            default=0,
        )
        for word in query_words
    ) / max(len(query_words), 1)
    return max(token_score, SequenceMatcher(None, normalized_query, title).ratio())


def detalle_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(
        Vehiculo.objects.select_related("modelo", "modelo__marca").prefetch_related(
            "fotografia_set"
        ),
        pk=vehiculo_id,
    )
    return render(request, "inventario/detalle.html", {"vehiculo": vehiculo})


@require_http_methods(["GET", "POST"])
def acceso(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("panel")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, "Esta cuenta no tiene permisos de administrador.")
        else:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next", "")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            return redirect("panel")

    return render(request, "inventario/acceso.html", {
        "form": form,
        "next": request.GET.get("next", ""),
    })


@require_POST
def salir(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("inicio")


@admin_requerido
def panel(request):
    now = timezone.localtime()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    week_start = (now - timedelta(days=now.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    month_sales = Venta.objects.filter(fecha_venta__gte=month_start, fecha_venta__lte=now)
    week_sales = Venta.objects.filter(fecha_venta__gte=week_start, fecha_venta__lte=now)
    grouped_sales = week_sales.values("fecha_venta__date").annotate(
        cantidad=Count("id_venta"), total=Sum("precio_venta")
    )
    by_day = {row["fecha_venta__date"]: row for row in grouped_sales}
    chart = []
    for offset, label in enumerate(("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")):
        date = week_start.date() + timedelta(days=offset)
        row = by_day.get(date, {})
        chart.append({
            "label": label,
            "total": row.get("total") or Decimal("0"),
            "cantidad": row.get("cantidad", 0),
        })
    highest_total = max((item["total"] for item in chart), default=Decimal("0"))
    for item in chart:
        item["height"] = int(item["total"] / highest_total * 100) if highest_total else 4

    context = {
        "ventas_mes": month_sales.count(),
        "ingresos_mes": month_sales.aggregate(total=Sum("precio_venta"))["total"] or Decimal("0"),
        "comision_mes": month_sales.aggregate(total=Sum("comision"))["total"] or Decimal("0"),
        "ventas_semana": week_sales.count(),
        "ingresos_semana": week_sales.aggregate(total=Sum("precio_venta"))["total"] or Decimal("0"),
        "vehiculos_disponibles": Vehiculo.objects.filter(estado="Disponible").count(),
        "ventas_recientes": Venta.objects.select_related("vehiculo__modelo__marca")[:8],
        "chart": chart,
    }
    return render(request, "inventario/panel.html", context)


@admin_requerido
def inventario_admin(request):
    vehiculos = Vehiculo.objects.select_related("modelo", "modelo__marca").order_by(
        "-fecha_publicacion"
    )
    return render(request, "inventario/inventario_admin.html", {"vehiculos": vehiculos})


def _form_inicial(vehiculo):
    return {
        "marca": vehiculo.modelo.marca.nombre,
        "modelo": vehiculo.modelo.nombre,
        "tipo": vehiculo.tipo,
        "anio": vehiculo.anio,
        "precio": vehiculo.precio,
        "kilometraje": vehiculo.kilometraje,
        "combustible": vehiculo.combustible,
        "transmision": vehiculo.transmision,
        "color": vehiculo.color,
        "blindaje": "1" if vehiculo.blindaje else ("0" if vehiculo.blindaje is False else ""),
        "cilindraje": vehiculo.cilindraje,
        "condicion": vehiculo.condicion,
        "tipo_precio": vehiculo.tipo_precio,
        "ultimo_digito_placa": vehiculo.ultimo_digito_placa,
        "asegurable": "1" if vehiculo.asegurable else ("0" if vehiculo.asegurable is False else ""),
        "descripcion": vehiculo.descripcion,
    }


def _validar_fotos(request, requeridas):
    fotos = request.FILES.getlist("fotos")
    if requeridas and not fotos:
        return "Selecciona al menos una fotografía del vehículo."
    if len(fotos) > 20:
        return "Puedes cargar hasta 20 fotografías por vehículo."
    for foto in fotos:
        if Path(foto.name).suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            return "Usa imágenes JPG, PNG o WEBP."
        if foto.size > 8 * 1024 * 1024:
            return "Cada fotografía debe pesar máximo 8 MB."
    return None


def _guardar_fotos(request, vehiculo):
    fotos = request.FILES.getlist("fotos")
    principal_nueva = request.POST.get("foto_principal_nueva", "")
    if principal_nueva.isdigit() and int(principal_nueva) < len(fotos):
        vehiculo.fotografia_set.update(es_principal=False)

    for index, foto in enumerate(request.FILES.getlist("fotos")):
        extension = Path(foto.name).suffix.lower()
        path = default_storage.save(f"vehiculos/{uuid4().hex}{extension}", foto)
        current_count = vehiculo.fotografia_set.count()
        Fotografia.objects.create(
            vehiculo=vehiculo,
            url_imagen=default_storage.url(path),
            es_principal=(
                index == int(principal_nueva)
                if principal_nueva.isdigit() and int(principal_nueva) < len(fotos)
                else current_count == 0 and index == 0
            ),
            orden=current_count + index,
        )


def _eliminar_fotos_seleccionadas(request, vehiculo):
    seleccionadas = request.POST.getlist("eliminar_fotos")
    fotos = vehiculo.fotografia_set.filter(id_foto__in=seleccionadas)
    for fotografia in fotos:
        url = fotografia.url_imagen
        if url.startswith(settings.MEDIA_URL):
            ruta = url.removeprefix(settings.MEDIA_URL).lstrip("/")
            if ruta.startswith("vehiculos/"):
                default_storage.delete(ruta)
        fotografia.delete()


def _marcar_foto_principal(request, vehiculo):
    nueva = request.POST.get("foto_principal_nueva", "")
    if nueva.isdigit() and int(nueva) < len(request.FILES.getlist("fotos")):
        return
    foto_id = request.POST.get("foto_principal")
    if not foto_id:
        return
    foto = vehiculo.fotografia_set.filter(id_foto=foto_id).first()
    if foto is None:
        return
    vehiculo.fotografia_set.update(es_principal=False)
    foto.es_principal = True
    foto.save(update_fields=["es_principal"])


def _copiar_datos_formulario(form, vehiculo):
    for field in (
        "tipo", "anio", "precio", "kilometraje", "combustible",
        "transmision", "color", "descripcion",
        "cilindraje", "condicion", "tipo_precio", "ultimo_digito_placa",
    ):
        setattr(vehiculo, field, form.cleaned_data[field])
    for field in ("blindaje", "asegurable"):
        value = form.cleaned_data[field]
        setattr(vehiculo, field, None if value == "" else value == "1")


def _buscar_o_crear_modelo(form):
    marca_nombre = form.cleaned_data["marca"].strip()
    marca = Marca.objects.filter(nombre__iexact=marca_nombre).first()
    if marca is None:
        marca = Marca.objects.create(nombre=marca_nombre)

    modelo_nombre = form.cleaned_data["modelo"].strip()
    modelo = Modelo.objects.filter(marca=marca, nombre__iexact=modelo_nombre).first()
    if modelo is None:
        modelo = Modelo.objects.create(marca=marca, nombre=modelo_nombre)
    return modelo


@admin_requerido
@require_http_methods(["GET", "POST"])
def crear_vehiculo(request):
    form = VehiculoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        error = _validar_fotos(request, requeridas=True)
        if error:
            form.add_error(None, error)
        else:
            with transaction.atomic():
                vehiculo = Vehiculo(
                    modelo=_buscar_o_crear_modelo(form),
                    estado="Disponible",
                    fecha_publicacion=timezone.now(),
                )
                _copiar_datos_formulario(form, vehiculo)
                vehiculo.save()
                _guardar_fotos(request, vehiculo)
            messages.success(request, "Vehículo publicado correctamente.")
            return redirect("inventario_admin")

    return render(request, "inventario/vehiculo_form.html", {
        "form": form,
        "titulo": "Publicar vehículo",
        "vehiculo": None,
    })


@admin_requerido
@require_http_methods(["GET", "POST"])
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(
        Vehiculo.objects.select_related("modelo__marca").prefetch_related("fotografia_set"),
        pk=vehiculo_id,
    )
    form = VehiculoForm(request.POST or None, initial=_form_inicial(vehiculo))
    if request.method == "POST" and form.is_valid():
        error = _validar_fotos(request, requeridas=False)
        if error:
            form.add_error(None, error)
        else:
            with transaction.atomic():
                vehiculo.modelo = _buscar_o_crear_modelo(form)
                _copiar_datos_formulario(form, vehiculo)
                vehiculo.save()
                _eliminar_fotos_seleccionadas(request, vehiculo)
                _guardar_fotos(request, vehiculo)
                _marcar_foto_principal(request, vehiculo)
            messages.success(request, "Los datos del vehículo se actualizaron.")
            return redirect("inventario_admin")

    return render(request, "inventario/vehiculo_form.html", {
        "form": form,
        "titulo": "Editar vehículo",
        "vehiculo": vehiculo,
    })


@admin_requerido
@require_http_methods(["GET", "POST"])
def registrar_venta(request):
    initial = {}
    selected_id = request.GET.get("vehiculo")
    if selected_id and selected_id.isdigit():
        selected_vehicle = Vehiculo.objects.filter(
            pk=selected_id, estado="Disponible"
        ).first()
        if selected_vehicle:
            initial = {
                "vehiculo_id": selected_vehicle.pk,
                "precio_venta": selected_vehicle.precio,
            }
    form = VentaForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                vehiculo = Vehiculo.objects.select_for_update().get(
                    pk=form.cleaned_data["vehiculo_id"], estado="Disponible"
                )
                precio = form.cleaned_data["precio_venta"]
                porcentaje = form.cleaned_data["porcentaje_comision"]
                comision = (precio * porcentaje / Decimal("100")).quantize(Decimal("0.01"))
                Venta.objects.create(
                    vehiculo=vehiculo,
                    precio_venta=precio,
                    porcentaje_comision=porcentaje,
                    comision=comision,
                )
                vehiculo.estado = "Vendido"
                vehiculo.save(update_fields=["estado"])
        except Vehiculo.DoesNotExist as error:
            form.add_error(None, "Este vehículo ya no está disponible para vender.")
        else:
            messages.success(request, "Venta registrada y vehículo marcado como vendido.")
            return redirect("panel")

    vehiculos = Vehiculo.objects.filter(estado="Disponible").select_related("modelo__marca")
    return render(request, "inventario/venta_form.html", {
        "form": form,
        "vehiculos": vehiculos,
    })
