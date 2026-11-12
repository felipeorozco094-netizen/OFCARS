type PanelVehicle = {
    id: string;
    titulo: string;
    tipo: string;
    marca: string;
    modelo: string;
    anio: number;
    precio: number;
    fotos: string[];
    estado: "Disponible" | "Vendido";
};

type VentaLocal = {
    vehiculoId: string;
    titulo: string;
    fecha: string;
    valor: number;
    comision: number;
};

const VEHICLES_KEY = "ofcars.vehiculos";
const SALES_KEY = "ofcars.ventas";
const money = (value: number): string => `$${value.toLocaleString("es-CO")}`;
const getVehicles = (): PanelVehicle[] => JSON.parse(localStorage.getItem(VEHICLES_KEY) || "[]");
const getSales = (): VentaLocal[] => JSON.parse(localStorage.getItem(SALES_KEY) || "[]");

document.addEventListener("DOMContentLoaded", () => {
    if (!document.body.classList.contains("pagina-admin")) return;

    const vehicles = getVehicles();
    const sales = getSales();
    const now = new Date();
    const monthSales = sales.filter((sale) => {
        const date = new Date(sale.fecha);
        return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear();
    });
    const monday = new Date(now);
    monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
    monday.setHours(0, 0, 0, 0);
    const weekSales = sales.filter((sale) => new Date(sale.fecha) >= monday);
    const monthRevenue = monthSales.reduce((sum, sale) => sum + sale.valor, 0);
    const monthCommission = monthSales.reduce((sum, sale) => sum + sale.comision, 0);

    document.querySelector("#ventas-mes")!.textContent = String(monthSales.length);
    document.querySelector("#ingresos-mes")!.textContent = money(monthRevenue);
    document.querySelector("#comision-mes")!.textContent = money(monthCommission);
    document.querySelector("#vehiculos-publicados")!.textContent = String(vehicles.length);
    document.querySelector("#vehiculos-disponibles")!.textContent = `${vehicles.filter((item) => item.estado === "Disponible").length} disponibles`;
    document.querySelector("#resumen-semana")!.textContent = `${weekSales.length} ventas · ${money(weekSales.reduce((sum, sale) => sum + sale.valor, 0))} en ingresos`;

    const inventory = document.querySelector<HTMLElement>("#lista-admin-vehiculos");
    if (inventory) {
        inventory.replaceChildren();
        vehicles.forEach((vehicle) => {
            const row = document.createElement("article");
            row.className = "admin-vehicle-row";
            const info = document.createElement("div");
            const title = document.createElement("strong");
            title.textContent = `${vehicle.titulo} · ${vehicle.anio}`;
            const status = document.createElement("small");
            status.textContent = `${vehicle.estado} · ${money(vehicle.precio)}`;
            info.append(title, status);
            row.append(info);

            if (vehicle.estado === "Disponible") {
                const sell = document.createElement("button");
                sell.type = "button";
                sell.className = "boton-secundario boton-vender";
                sell.textContent = "Registrar venta";
                sell.addEventListener("click", () => {
                    const amount = Number(window.prompt("¿Por cuánto se vendió?", String(vehicle.precio)));
                    if (!Number.isFinite(amount) || amount <= 0) return;
                    const commissionRate = Number(window.prompt("Porcentaje de comisión del concesionario", "5"));
                    if (!Number.isFinite(commissionRate) || commissionRate < 0 || commissionRate > 100) return;

                    const currentVehicles = getVehicles();
                    const currentVehicle = currentVehicles.find((item) => item.id === vehicle.id);
                    if (!currentVehicle) return;
                    currentVehicle.estado = "Vendido";
                    localStorage.setItem(VEHICLES_KEY, JSON.stringify(currentVehicles));
                    const currentSales = getSales();
                    currentSales.unshift({
                        vehiculoId: vehicle.id,
                        titulo: vehicle.titulo,
                        fecha: new Date().toISOString(),
                        valor: amount,
                        comision: amount * commissionRate / 100,
                    });
                    localStorage.setItem(SALES_KEY, JSON.stringify(currentSales));
                    window.location.reload();
                });
                row.append(sell);
            }
            inventory.append(row);
        });
        if (!vehicles.length) inventory.innerHTML = '<p class="sin-vehiculos">Todavía no hay publicaciones. Usa “Publicar un vehículo” para empezar.</p>';
    }

    const salesTable = document.querySelector<HTMLElement>("#tabla-ventas-recientes");
    const emptySales = document.querySelector<HTMLElement>("#sin-ventas");
    if (salesTable) {
        salesTable.replaceChildren();
        sales.slice(0, 8).forEach((sale) => {
            const row = document.createElement("tr");
            [sale.titulo, new Date(sale.fecha).toLocaleDateString("es-CO"), money(sale.valor), "Completada"].forEach((value) => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.append(cell);
            });
            salesTable.append(row);
        });
        if (emptySales) emptySales.hidden = sales.length > 0;
    }
});
