"use strict";
const carousel = document.querySelector("[data-interest-carousel]");
if (carousel) {
    const scrollCarousel = (direction) => {
        const firstCard = carousel.querySelector(".interest-card");
        const gap = Number.parseFloat(getComputedStyle(carousel).columnGap) || 0;
        carousel.scrollBy({
            left: direction * ((firstCard?.getBoundingClientRect().width ?? 200) + gap),
            behavior: "smooth",
        });
    };
    document.querySelector("[data-carousel-prev]")
        ?.addEventListener("click", () => scrollCarousel(-1));
    document.querySelector("[data-carousel-next]")
        ?.addEventListener("click", () => scrollCarousel(1));
}
