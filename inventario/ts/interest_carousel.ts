const carousel = document.querySelector<HTMLElement>("[data-interest-carousel]");

if (carousel) {
    const scrollCarousel = (direction: -1 | 1) => {
        const firstCard = carousel.querySelector<HTMLElement>(".interest-card");
        const gap = Number.parseFloat(getComputedStyle(carousel).columnGap) || 0;
        carousel.scrollBy({
            left: direction * ((firstCard?.getBoundingClientRect().width ?? 200) + gap),
            behavior: "smooth",
        });
    };

    document.querySelector<HTMLButtonElement>("[data-carousel-prev]")
        ?.addEventListener("click", () => scrollCarousel(-1));
    document.querySelector<HTMLButtonElement>("[data-carousel-next]")
        ?.addEventListener("click", () => scrollCarousel(1));
}
