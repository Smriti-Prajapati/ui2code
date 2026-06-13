document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const input = document.getElementById("imageInput");
    const preview = document.getElementById("preview");
    const dropzone = document.getElementById("dropzone");
    const status = document.getElementById("uploadStatus");
    const studioState = document.getElementById("studioState");
    const scanPanel = document.getElementById("scanPanel");
    const progressBar = document.getElementById("progressBar");
    const pipelineList = document.getElementById("pipelineList");
    const revealItems = document.querySelectorAll(".reveal");

    if (!uploadBtn || !input) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.14 });

    revealItems.forEach((item) => observer.observe(item));

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
        uploadBtn.textContent = "Generating...";
        setStatus("Scanning screenshot and preparing generated project.", false);
        setStudioState("Scanning");
        await runPipelineAnimation();

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
        if (scanPanel) scanPanel.classList.add("is-visible");
        if (progressBar) progressBar.style.width = "12%";
        activatePipelineStep(0);
        setStudioState("Loaded");
        setStatus(`${file.name} selected. Ready to generate.`, false);
    }

    function setStatus(message, isError) {
        if (!status) return;
        status.textContent = message;
        status.style.color = isError ? "#b91c1c" : "";
    }

    function setStudioState(message) {
        if (!studioState) return;
        studioState.textContent = message;
    }

    function activatePipelineStep(index) {
        if (!pipelineList) return;

        [...pipelineList.children].forEach((item, itemIndex) => {
            item.classList.toggle("active", itemIndex <= index);
        });
    }

    function runPipelineAnimation() {
        if (!scanPanel || !progressBar || !pipelineList) return Promise.resolve();

        scanPanel.classList.add("is-visible");
        const steps = [...pipelineList.children];
        const progressValues = [18, 34, 52, 70, 88, 100];

        return new Promise((resolve) => {
            steps.forEach((_, index) => {
                window.setTimeout(() => {
                    activatePipelineStep(index);
                    progressBar.style.width = `${progressValues[index]}%`;
                    setStatus(`${steps[index].textContent} complete.`, false);

                    if (index === steps.length - 1) {
                        window.setTimeout(resolve, 260);
                    }
                }, index * 260);
            });
        });
    }
});
