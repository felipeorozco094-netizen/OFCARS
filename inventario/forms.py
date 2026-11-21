from django import forms

from .models import Vehiculo


class VehiculoForm(forms.Form):
    marca = forms.CharField(max_length=80, label="Marca")
    modelo = forms.CharField(max_length=100, label="Modelo")
    tipo = forms.ChoiceField(choices=Vehiculo.TIPOS, label="Tipo de vehículo")
    anio = forms.IntegerField(min_value=1950, max_value=2100, label="Año")
    precio = forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=0,
        label="Precio (COP)",
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "autocomplete": "off",
            "data-currency-input": "cop",
            "placeholder": "0",
        }),
    )
    kilometraje = forms.IntegerField(
        min_value=0,
        initial=0,
        label="Kilometraje",
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "autocomplete": "off",
            "data-number-format": "thousands",
            "placeholder": "Ej. 85.000",
        }),
    )
    combustible = forms.ChoiceField(choices=Vehiculo.COMBUSTIBLES, label="Combustible")
    transmision = forms.ChoiceField(choices=Vehiculo.TRANSMISIONES, label="Transmisión")
    color = forms.CharField(max_length=50, required=False, label="Color")
    blindaje = forms.ChoiceField(choices=(("", "Sin especificar"), ("1", "Sí"), ("0", "No")), required=False, label="Blindaje")
    cilindraje = forms.IntegerField(min_value=0, required=False, label="Cilindraje (cc)")
    condicion = forms.ChoiceField(choices=Vehiculo.CONDICIONES, required=False, label="Estado del vehículo")
    tipo_precio = forms.ChoiceField(choices=Vehiculo.TIPOS_PRECIO, required=False, label="Tipo de precio")
    ultimo_digito_placa = forms.RegexField(regex=r"^\d$", max_length=1, required=False, label="Último dígito de placa")
    asegurable = forms.ChoiceField(choices=(("", "Sin especificar"), ("1", "Sí, asegurable"), ("0", "No")), required=False, label="Peritaje / Asegurable")
    descripcion = forms.CharField(
        required=False,
        label="Descripción",
        widget=forms.Textarea(attrs={"rows": 5}),
    )


class VentaForm(forms.Form):
    vehiculo_id = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    precio_venta = forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        min_value=1,
        label="Precio de venta (COP)",
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "autocomplete": "off",
            "data-currency-input": "cop",
            "placeholder": "0",
        }),
    )
    porcentaje_comision = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        initial=5,
        label="Comisión del concesionario (%)",
    )
