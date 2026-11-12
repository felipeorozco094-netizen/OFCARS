type Publicacion = {
    id: string;
    titulo: string;
    tipo: string;
    marca: string;
    modelo: string;
    anio: number;
    precio: number;
    kilometraje: number;
    combustible: string;
    transmision: string;
    color: string;
    descripcion: string;
    fotos: string[];
    estado: "Disponible" | "Vendido";
    fecha: string;
};

const STORAGE_VEHICULOS = "ofcars.vehiculos";

function leerVehiculos(): Publicacion[] {
    return JSON.parse(localStorage.getItem(STORAGE_VEHICULOS) || "[]") as Publicacion[];
}

function convertirFoto(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result));
        reader.onerror = () => reject(new Error(`No se pudo leer ${file.name}`));
        reader.readAsDataURL(file);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector<HTMLFormElement>("#form-vehiculo");
    const input = document.querySelector<HTMLInputElement>("#fotos");
    const zone = document.querySelector<HTMLElement>("#zona-fotos");
    const list = document.querySelector<HTMLElement>("#lista-fotos");
    const message = document.querySelector<HTMLElement>("#mensaje-formulario");
    const preview = document.querySelector<HTMLElement>("#vista-previa-anuncio");
    if (!form || !input || !zone || !list || !message || !preview) return;

    let selectedFiles: File[] = [];

    const renderPhotos = (): void => {
        list.replaceChildren();
        selectedFiles.forEach((file, index) => {
            const card = document.createElement("div");
            card.className = "foto-carga";
            const image = document.createElement("img");
            image.src = URL.createObjectURL(file);
            image.alt = file.name;
            const caption = document.createElement("span");
            caption.textContent = index === 0 ? "Foto principal" : file.name;
            const remove = document.createElement("button");
            remove.type = "button";
            remove.className = "quitar-foto";
            remove.textContent = "×";
            remove.setAttribute("aria-label", `Quitar ${file.name}`);
            remove.addEventListener("click", () => {
                selectedFiles = selectedFiles.filter((_, fileIndex) => fileIndex !== index);
                renderPhotos();
            });
            card.append(image, caption, remove);
            list.append(card);
        });
    };

    const addFiles = (files: FileList | File[]): void => {
        const photos = Array.from(files).filter((file) => file.type.startsWith("image/"));
        selectedFiles = [...selectedFiles, ...photos].filter(
            (file, index, all) => all.findIndex((item) => item.name === file.name && item.size === file.size) === index
        );
        renderPhotos();
    };

    input.addEventListener("change", () => addFiles(input.files ?? []));
    ["dragenter", "dragover"].forEach((name) => zone.addEventListener(name, (event) => {
        event.preventDefault();
        zone.classList.add("arrastrando");
    }));
    ["dragleave", "drop"].forEach((name) => zone.addEventListener(name, (event) => {
        event.preventDefault();
        zone.classList.remove("arrastrando");
    }));
    zone.addEventListener("drop", (event) => {
        const dragEvent = event as DragEvent;
        if (dragEvent.dataTransfer) addFiles(dragEvent.dataTransfer.files);
    });

    form.addEventListener("input", () => { message.hidden = true; });
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!form.reportValidity()) return;
        if (!selectedFiles.length) {
            message.textContent = "Agrega al menos una foto para publicar el vehículo.";
            message.hidden = false;
            return;
        }

        const totalBytes = selectedFiles.reduce((total, file) => total + file.size, 0);
        if (totalBytes > 3_000_000) {
            message.textContent = "Para esta maqueta, selecciona fotos que en total pesen menos de 3 MB.";
            message.hidden = false;
            return;
        }

        try {
            const data = new FormData(form);
            const brand = String(data.get("marca") || "").trim();
            const model = String(data.get("modelo") || "").trim();
            const photos = await Promise.all(selectedFiles.map(convertirFoto));
            const vehicle: Publicacion = {
                id: `local-${Date.now()}`,
                titulo: `${brand} ${model}`,
                tipo: String(data.get("tipo") || ""),
                marca: brand,
                modelo: model,
                anio: Number(data.get("anio")),
                precio: Number(data.get("precio")),
                kilometraje: Number(data.get("kilometraje") || 0),
                combustible: String(data.get("combustible") || ""),
                transmision: String(data.get("transmision") || ""),
                color: String(data.get("color") || ""),
                descripcion: String(data.get("descripcion") || ""),
                fotos: photos,
                estado: "Disponible",
                fecha: new Date().toISOString(),
            };

            const vehicles = leerVehiculos();
            vehicles.push(vehicle);
            localStorage.setItem(STORAGE_VEHICULOS, JSON.stringify(vehicles));
            message.textContent = "¡Vehículo publicado! Ya aparece en el catálogo y en el panel.";
            message.hidden = false;
            window.setTimeout(() => { window.location.href = "admin.html"; }, 900);
        } catch {
            message.textContent = "No se pudo guardar. Reduce el tamaño de las fotos y vuelve a intentarlo.";
            message.hidden = false;
        }
    });
});
