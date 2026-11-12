const fileInput = document.querySelector<HTMLInputElement>("#photo-input");
const preview = document.querySelector<HTMLDivElement>("#photo-preview");
const countLabel = document.querySelector<HTMLElement>("#photo-count");
const dropArea = document.querySelector<HTMLLabelElement>("#upload-drop");

if (fileInput && preview && countLabel && dropArea) {
    const renderFiles = (files: FileList | File[]) => {
        preview.replaceChildren();

        const images = Array.from(files).filter((file) => file.type.startsWith("image/"));
        images.forEach((file) => {
            const image = document.createElement("img");
            image.src = URL.createObjectURL(file);
            image.alt = `Vista previa: ${file.name}`;
            preview.append(image);
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
        if (!droppedFiles) return;

        fileInput.files = droppedFiles;
        renderFiles(droppedFiles);
    });
}
