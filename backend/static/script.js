document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const input = document.getElementById("imageInput");
    const preview = document.getElementById("preview");
    const dropzone = document.getElementById("dropzone");
    const status = document.getElementById("uploadStatus");

    if (!uploadBtn || !input) return;

    input.addEventListener("change", () => {
        const file = input.files[0];
        showPreview(file);
    });

    if (dropzone) {
        ["dragenter", "dragover"].forEach((eventName) => {
            dropzone.addEventListener(eventName, (event) => {
                event.preventDefault();
                dropzone.classList.add("is-dragging");
            });
        });

        ["dragleave", "drop"].forEach((eventName) => {
            dropzone.addEventListener(eventName, (event) => {
                event.preventDefault();
                dropzone.classList.remove("is-dragging");
            });
        });

        dropzone.addEventListener("drop", (event) => {
            const file = event.dataTransfer.files[0];
            if (!file) return;

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            showPreview(file);
        });
    }

    uploadBtn.addEventListener("click", async function () {
        const file = input.files[0];

        if (!file) {
            setStatus("Choose a screenshot first.", true);
            return;
        }

        const formData = new FormData();
        formData.append("image", file);

        uploadBtn.disabled = true;
        uploadBtn.textContent = "Uploading...";
        setStatus("Uploading screenshot and preparing analysis workspace.", false);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Upload failed.");
            }

            window.location.href = data.redirect_url;
        } catch (error) {
            uploadBtn.disabled = false;
            uploadBtn.textContent = "Generate UI System";
            setStatus(error.message, true);
        }
    });

    function showPreview(file) {
        if (!file) return;

        if (!file.type.startsWith("image/")) {
            setStatus("Please select an image file.", true);
            return;
        }

        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
        setStatus(`${file.name} selected. Ready to generate.`, false);
    }

    function setStatus(message, isError) {
        if (!status) return;
        status.textContent = message;
        status.style.color = isError ? "#b91c1c" : "";
    }
});
