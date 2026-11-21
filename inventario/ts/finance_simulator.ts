const simulator = document.querySelector<HTMLElement>(".finance-simulator");

if (simulator) {
    const rawPrice = simulator.dataset.price ?? "";
    const hasDecimalCents = /[.,]\d{1,2}$/.test(rawPrice);
    const priceDigits = rawPrice.replace(/\D/g, "");
    const price = Number(priceDigits) / (hasDecimalCents ? 100 : 1);
    const vehicleName = simulator.dataset.vehicle ?? "este vehículo";
    const monthsButtons = Array.from(
        simulator.querySelectorAll<HTMLButtonElement>("[data-months]")
    );
    const downPayment = simulator.querySelector<HTMLInputElement>("#down-payment");
    const carPriceOutput = simulator.querySelector<HTMLElement>("[data-car-price]");
    const downPaymentOutput = simulator.querySelector<HTMLOutputElement>("[data-down-payment]");
    const downPercentOutput = simulator.querySelector<HTMLOutputElement>("[data-down-percent]");
    const monthlyOutput = simulator.querySelector<HTMLElement>("[data-monthly-payment]");
    const contactLink = simulator.querySelector<HTMLAnchorElement>("[data-finance-contact]");
    const cop = new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        maximumFractionDigits: 0,
    });
    let selectedMonths = 72;

    const update = () => {
        if (!downPayment || !carPriceOutput || !downPaymentOutput || !downPercentOutput || !monthlyOutput) return;

        const percent = Number(downPayment.value);
        const initialPayment = price * percent / 100;
        const financedAmount = price - initialPayment;
        const monthlyRate = Math.pow(1 + 0.22, 1 / 12) - 1;
        const payment = financedAmount === 0
            ? 0
            : financedAmount * monthlyRate / (1 - Math.pow(1 + monthlyRate, -selectedMonths));

        carPriceOutput.textContent = cop.format(price);
        downPaymentOutput.textContent = cop.format(initialPayment);
        downPercentOutput.textContent = `${percent} %`;
        monthlyOutput.textContent = cop.format(payment);

        if (contactLink) {
            const message = `Hola, quiero recibir información de financiación para ${vehicleName}.`;
            contactLink.href = `https://wa.me/573001234567?text=${encodeURIComponent(message)}`;
        }
    };

    monthsButtons.forEach((button) => {
        button.addEventListener("click", () => {
            selectedMonths = Number(button.dataset.months);
            monthsButtons.forEach((option) => {
                const active = option === button;
                option.classList.toggle("is-active", active);
                option.setAttribute("aria-pressed", String(active));
            });
            update();
        });
    });

    downPayment?.addEventListener("input", update);
    monthsButtons.forEach((button) => {
        button.setAttribute("aria-pressed", String(Number(button.dataset.months) === selectedMonths));
    });
    update();
}
