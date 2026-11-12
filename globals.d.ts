type DetalleCatalogo = {
    brand: string;
    model: string;
    name: string;
    year: number;
    price: number;
    category: string;
    description: string;
    mileage: string;
    fuel: string;
    transmission: string;
    images: string[];
};

interface Window {
    OF_CARS_VEHICULOS?: Record<string, DetalleCatalogo>;
}
