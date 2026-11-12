document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form-busqueda");
  if (!form) return;

  const cards = [...document.querySelectorAll(".tarjeta[data-categoria]")];
  const brand = form.elements.marca;
  const model = form.elements.modelo;
  const queryInput = form.elements.buscar;
  const message = document.getElementById("mensaje-sin-resultados");
  const originalOrder = new Map(cards.map((card, index) => [card, index]));
  const originalGrid = new Map(cards.map((card) => [card, card.closest(".tarjetas")]));

  // Enlaza cada publicación con su ficha de detalle.
  cards.forEach((card) => {
    if (!card.dataset.id || card.closest("a.enlace-tarjeta")) return;

    const link = document.createElement("a");
    link.className = "enlace-tarjeta";
    link.href = `vehiculo.html?id=${encodeURIComponent(card.dataset.id)}`;
    card.before(link);
    link.append(card);
  });

  // Ignora tildes, mayúsculas, signos y espacios repetidos.
  function normalize(value = "") {
    return value
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("es")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  function unique(values) {
    return [...new Set(values.filter(Boolean))]
      .sort((first, second) => first.localeCompare(second, "es"));
  }

  function fillSelect(select, label, values, selected = "") {
    select.replaceChildren(new Option(label, ""));
    values.forEach((value) => select.add(new Option(value, value)));
    select.value = values.includes(selected) ? selected : "";
  }

  function updateModels() {
    const selectedModel = model.value;
    const availableModels = unique(
      cards
        .filter((card) => !brand.value || card.dataset.marca === brand.value)
        .map((card) => card.dataset.modelo)
    );

    fillSelect(model, "Todos los modelos", availableModels, selectedModel);
  }

  function getNumber(name) {
    const value = form.elements[name]?.value.trim();
    return value ? Number(value) : null;
  }

  // Calcula qué tanto coincide la consulta con el título publicado.
  function titleScore(card, query) {
    if (!query) return 0;

    const title = normalize(card.querySelector("h3")?.textContent);
    const description = normalize(card.querySelector(".info-auto p")?.textContent);
    const searchText = `${title} ${description}`;

    if (title === query) return 100;
    if (title.includes(query)) return 80;
    if (searchText.includes(query)) return 65;

    const queryWords = query.split(" ");
    const titleWords = title.split(" ");
    let matchedWords = 0;

    queryWords.forEach((word) => {
      const exactOrPartialMatch = titleWords.some((titleWord) =>
        titleWord.includes(word) || word.includes(titleWord)
      );

      const smallTypoMatch = titleWords.some((titleWord) =>
        titleWord.length >= 5 &&
        word.length >= 5 &&
        editDistanceAtMostOne(titleWord, word)
      );

      if (exactOrPartialMatch || smallTypoMatch) matchedWords += 1;
    });

    return queryWords.length ? (matchedWords / queryWords.length) * 50 : 0;
  }

  // Tolera una letra distinta u omitida en palabras largas.
  function editDistanceAtMostOne(first, second) {
    if (Math.abs(first.length - second.length) > 1) return false;

    let firstIndex = 0;
    let secondIndex = 0;
    let differences = 0;

    while (firstIndex < first.length && secondIndex < second.length) {
      if (first[firstIndex] === second[secondIndex]) {
        firstIndex += 1;
        secondIndex += 1;
        continue;
      }

      differences += 1;
      if (differences > 1) return false;

      if (first.length > second.length) firstIndex += 1;
      else if (second.length > first.length) secondIndex += 1;
      else {
        firstIndex += 1;
        secondIndex += 1;
      }
    }

    if (firstIndex < first.length || secondIndex < second.length) differences += 1;
    return differences <= 1;
  }

  function runSearch(event) {
    event?.preventDefault();

    const query = normalize(queryInput?.value);
    const selectedCategory =
      form.querySelector('input[name="categoria"]:checked')?.value || "";
    // Al buscar texto, no dejamos que la categoría preseleccionada esconda otros títulos.
    const category = query ? "" : selectedCategory;
    const brandValue = normalize(brand.value);
    const modelValue = normalize(model.value);
    const minPrice = getNumber("precio_min");
    const maxPrice = getNumber("precio_max");
    const minYear = getNumber("anio_min");
    const maxYear = getNumber("anio_max");
    const preferences = ["permuta", "promocion", "blindaje"]
      .filter((name) => form.elements[name]?.checked);
    const matches = [];

    cards.forEach((card) => {
      const price = Number(card.dataset.precio);
      const year = Number(card.dataset.anio);
      const score = titleScore(card, query);
      const categoryMatch = !category || card.dataset.categoria === category;
      const brandMatch = !brandValue || normalize(card.dataset.marca) === brandValue;
      const modelMatch = !modelValue || normalize(card.dataset.modelo) === modelValue;
      const priceMatch =
        (minPrice === null || price >= minPrice) &&
        (maxPrice === null || price <= maxPrice);
      const yearMatch =
        (minYear === null || year >= minYear) &&
        (maxYear === null || year <= maxYear);
      const preferencesMatch = preferences.every(
        (name) => card.dataset[name] === "true"
      );
      const titleMatch = !query || score > 0;
      const visible =
        categoryMatch && brandMatch && modelMatch &&
        priceMatch && yearMatch && preferencesMatch && titleMatch;

      card.hidden = !visible;
      const link = card.closest(".enlace-tarjeta");
      if (link) link.hidden = !visible;
      if (visible) matches.push({ card, score });
    });

    // Ordena por similitud dentro de cada categoría, conservando la estructura de secciones.
    if (query) {
      matches
        .sort((first, second) =>
          second.score - first.score ||
          originalOrder.get(first.card) - originalOrder.get(second.card)
        )
        .forEach(({ card }) => {
          const grid = originalGrid.get(card);
          const link = card.closest(".enlace-tarjeta");
          if (grid) grid.append(link || card);
        });
    }

    document.querySelectorAll(".seccion-vehiculos").forEach((section) => {
      const hasVisibleCard = section.querySelector(
        ".tarjeta[data-categoria]:not([hidden])"
      );
      const hasEmptyMessage = section.querySelector(".sin-vehiculos");
      section.hidden = !hasVisibleCard && !hasEmptyMessage;
    });

    if (message) message.hidden = matches.length > 0;
    document.getElementById("resultados")?.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  }

  form.addEventListener("submit", runSearch);
  brand.addEventListener("change", updateModels);

  queryInput?.addEventListener("input", () => {
    if (queryInput.value.trim() === "") runSearch();
  });

  updateModels();
});

