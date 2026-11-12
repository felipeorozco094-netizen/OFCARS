type CatalogVehicle = {
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
    descripcion: string;
    fotos: string[];
    estado: string;
};

document.addEventListener("DOMContentLoaded", () => {
    const vehicles = JSON.parse(localStorage.getItem("ofcars.vehiculos") || "[]") as CatalogVehicle[];
    vehicles.filter((vehicle) => vehicle.estado === "Disponible").forEach((vehicle) => {
        window.OF_CARS_VEHICULOS ??= {};
        window.OF_CARS_VEHICULOS[vehicle.id] = {
            brand: vehicle.marca,
            model: vehicle.modelo,
            name: vehicle.titulo,
            year: vehicle.anio,
            price: vehicle.precio,
            category: vehicle.tipo,
            description: vehicle.descripcion || "",
            mileage: `${vehicle.kilometraje.toLocaleString("es-CO")} km`,
            fuel: vehicle.combustible || "Por confirmar",
            transmission: vehicle.transmision || "Por confirmar",
            images: vehicle.fotos,
        };
        const category = vehicle.tipo === "Carro" ? "carros"
            : vehicle.tipo === "Camioneta" ? "camionetas"
            : vehicle.tipo === "Camión" ? "camiones" : "otros";
        const section = document.querySelector<HTMLElement>(`#${category} .tarjetas`);
        if (!section) return;

        const card = document.createElement("article");
        card.className = "tarjeta";
        card.dataset.categoria = category;
        card.dataset.marca = vehicle.marca;
        card.dataset.modelo = vehicle.modelo;
        card.dataset.anio = String(vehicle.anio);
        card.dataset.precio = String(vehicle.precio);
        card.dataset.permuta = "false";
        card.dataset.promocion = "false";
        card.dataset.blindaje = "false";
        card.dataset.id = vehicle.id;
        if (vehicle.fotos[0]) {
            const image = document.createElement("img");
            image.className = "imagencars";
            image.src = vehicle.fotos[0];
            image.alt = vehicle.titulo;
            card.append(image);
        }
        const info = document.createElement("div");
        info.className = "info-auto";
        const title = document.createElement("h3");
        title.textContent = vehicle.titulo;
        const description = document.createElement("p");
        description.textContent = `${vehicle.modelo} · ${vehicle.anio} · ${vehicle.kilometraje} km`;
        const price = document.createElement("span");
        price.className = "precio";
        price.textContent = `$${vehicle.precio.toLocaleString("es-CO")}`;
        info.append(title, description, price);
        card.append(info);
        section.append(card);
    });
});
