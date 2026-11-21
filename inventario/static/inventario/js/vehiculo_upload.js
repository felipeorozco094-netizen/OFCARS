"use strict";
const fileInput = document.querySelector("#photo-input");
const preview = document.querySelector("#photo-preview");
const countLabel = document.querySelector("#photo-count");
const dropArea = document.querySelector("#upload-drop");
const currencyInput = document.querySelector('[data-currency-input="cop"]');
const mileageInput = document.querySelector('[data-number-format="thousands"]');
function formatWholeNumber(input) {
    const digits = input.value.replace(/\D/g, "");
    input.value = digits ? Number(digits).toLocaleString("es-CO") : "";
}
if (mileageInput) {
    mileageInput.addEventListener("input", () => formatWholeNumber(mileageInput));
    mileageInput.form?.addEventListener("submit", () => {
        mileageInput.value = mileageInput.value.replace(/\D/g, "");
    });
    formatWholeNumber(mileageInput);
}
if (currencyInput) {
    const formatPesos = () => {
        const digits = currencyInput.value.replace(/\D/g, "");
        currencyInput.value = digits ? Number(digits).toLocaleString("es-CO") : "";
    };
    currencyInput.addEventListener("input", formatPesos);
    currencyInput.form?.addEventListener("submit", () => {
        currencyInput.value = currencyInput.value.replace(/\D/g, "");
    });
    formatPesos();
}
if (fileInput && preview && countLabel && dropArea) {
    const renderFiles = (files) => {
        preview.replaceChildren();
        const images = Array.from(files).filter((file) => file.type.startsWith("image/"));
        images.forEach((file, index) => {
            const card = document.createElement("label");
            card.className = "new-photo-choice";
            const image = document.createElement("img");
            image.src = URL.createObjectURL(file);
            image.alt = `Vista previa: ${file.name}`;
            const choice = document.createElement("span");
            choice.className = "photo-choice";
            const radio = document.createElement("input");
            radio.type = "radio";
            radio.name = "foto_principal_nueva";
            radio.value = String(index);
            radio.checked = index === 0;
            choice.append(radio, document.createTextNode("Usar como foto principal"));
            card.append(image, choice);
            preview.append(card);
        });
        countLabel.textContent = images.length
            ? `${images.length} foto${images.length === 1 ? "" : "s"} seleccionada${images.length === 1 ? "" : "s"}.`
            : "No has seleccionado fotos nuevas.";
    };
    fileInput.addEventListener("change", () => renderFiles(fileInput.files ?? []));
    dropArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropArea.classList.add("is-dragging");
    });
    dropArea.addEventListener("dragleave", () => dropArea.classList.remove("is-dragging"));
    dropArea.addEventListener("drop", (event) => {
        event.preventDefault();
        dropArea.classList.remove("is-dragging");
        const droppedFiles = event.dataTransfer?.files;
        if (!droppedFiles)
            return;
        fileInput.files = droppedFiles;
        renderFiles(droppedFiles);
    });
}
