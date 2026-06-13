document.addEventListener("DOMContentLoaded", function () {
    const imageFile = document.body.dataset.imageFile;
    const analyzeBtn = document.getElementById("analyzeBtn");
    const statusBar = document.getElementById("statusBar");
    const metricsGrid = document.getElementById("metricsGrid");
    const hierarchyOutput = document.getElementById("hierarchyOutput");
    const designOutput = document.getElementById("designOutput");
    const layoutOutput = document.getElementById("layoutOutput");
    const rawOutput = document.getElementById("rawOutput");
    const paletteOutput = document.getElementById("paletteOutput");
    const fileSelect = document.getElementById("fileSelect");
    const codeOutput = document.getElementById("codeOutput");
    const stagePill = document.getElementById("stagePill");
    const sourceScreenshot = document.getElementById("sourceScreenshot");
    const directFileWarning = document.getElementById("directFileWarning");

    let generatedFiles = {};
    const isTemplatePreview = !imageFile || imageFile.includes("{");

    if (isTemplatePreview || window.location.protocol === "file:") {
        analyzeBtn.disabled = true;
        statusBar.textContent = "Open http://127.0.0.1:5000 and upload a screenshot to use the studio.";
        stagePill.textContent = "Server required";
        directFileWarning.style.display = "block";
        sourceScreenshot.style.display = "none";
    }

    document.querySelectorAll(".tab").forEach((tab) => {
        tab.addEventListener("click", () => {
            document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
            document.querySelectorAll(".panel").forEach((item) => item.classList.remove("active"));
            tab.classList.add("active");
            document.getElementById(`${tab.dataset.tab}Panel`).classList.add("active");
        });
    });

    fileSelect.addEventListener("change", () => {
        codeOutput.value = generatedFiles[fileSelect.value] || "";
    });

    analyzeBtn.addEventListener("click", analyzeScreenshot);

    async function analyzeScreenshot() {
        if (isTemplatePreview) return;

        setLoading(true);
        stagePill.textContent = "Running";
        statusBar.textContent = "Running visual understanding, OCR, layout analysis, reasoning, and code generation...";

        try {
            const response = await fetch(`/api/analyze/${encodeURIComponent(imageFile)}?framework=nextjs&styling=tailwind`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Analysis failed");
            }

            renderAnalysis(data);
            statusBar.textContent = `Analysis complete: ${data.visual_understanding.component_count} components, ${data.ocr_semantics.text_elements.length} text blocks`;
            stagePill.textContent = "Complete";
        } catch (error) {
            statusBar.textContent = error.message;
            stagePill.textContent = "Error";
        } finally {
            setLoading(false);
        }
    }

    function setLoading(isLoading) {
        analyzeBtn.disabled = isLoading;
        analyzeBtn.textContent = isLoading ? "Analyzing..." : "Analyze Screenshot";
    }

    function renderAnalysis(data) {
        renderMetrics(data.evaluation);
        hierarchyOutput.textContent = JSON.stringify(data.component_hierarchy, null, 2);
        designOutput.textContent = JSON.stringify(data.design_system, null, 2);
        layoutOutput.textContent = JSON.stringify(data.layout_intelligence, null, 2);
        rawOutput.textContent = JSON.stringify(data, null, 2);
        renderPalette(data.design_system.colors.all_colors || []);
        renderFiles(data.generated_project.files || {});
    }

    function renderMetrics(evaluation) {
        const labels = {
            component_detection_accuracy: "Components",
            ocr_accuracy: "OCR",
            layout_reconstruction_accuracy: "Layout",
            visual_similarity_score: "Visual",
            code_quality_score: "Code",
            overall_score: "Overall",
        };

        metricsGrid.innerHTML = Object.entries(labels)
            .map(([key, label]) => {
                const value = Math.round((evaluation[key] || 0) * 100);
                return `<div class="metric"><span>${label}</span><strong>${value}%</strong></div>`;
            })
            .join("");
    }

    function renderPalette(colors) {
        paletteOutput.innerHTML = colors
            .map((color) => (
                `<div class="swatch" title="${color.hex}">
                    <span style="background:${color.hex}"></span>
                    <small>${color.hex}</small>
                </div>`
            ))
            .join("");
    }

    function renderFiles(files) {
        generatedFiles = files;
        fileSelect.innerHTML = Object.keys(files)
            .map((path) => `<option value="${path}">${path}</option>`)
            .join("");

        const firstFile = Object.keys(files)[0];
        codeOutput.value = firstFile ? files[firstFile] : "";
    }
});
