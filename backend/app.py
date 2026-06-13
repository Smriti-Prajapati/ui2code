from __future__ import annotations

import json
import os
import zipfile
from io import BytesIO

from flask import Flask, jsonify, render_template, request, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from code_gen_engine import CodeGenerator
from config import Config
from pipeline import UI2CodePipeline


app = Flask(__name__)
app.config.from_object(Config)
app.config["MAX_CONTENT_LENGTH"] = Config.MAX_FILE_SIZE
Config.init_app(app)
CORS(app)

pipeline = None


def get_pipeline() -> UI2CodePipeline:
    global pipeline
    if pipeline is None:
        pipeline = UI2CodePipeline()
    return pipeline


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def build_project_readme(result: dict) -> str:
    image = result.get("image", {})
    evaluation = result.get("evaluation", {})
    files = result.get("generated_project", {}).get("files", {})

    return f"""# UI2CODE Generated Project

This project was generated from a UI screenshot using visual understanding, OCR semantics, layout intelligence, design-system extraction, hierarchy reasoning, and code generation.

## Source

- Screenshot: {image.get("filename", "uploaded image")}
- Size: {image.get("width", "-")}x{image.get("height", "-")}
- Components detected: {result.get("visual_understanding", {}).get("component_count", 0)}
- Overall evaluation score: {evaluation.get("overall_score", 0)}

## Run the Next.js project

```bash
npm install
npm run dev
```

## Included

- `project/`: deployable Next.js + Tailwind project files
- `static-html/`: standalone HTML/CSS/JS fallback
- `analysis/`: hierarchy, design system, layout intelligence, OCR semantics, and evaluation JSON
- `assets/`: original screenshot

## Generated files

{chr(10).join(f"- `{path}`" for path in sorted(files))}
"""


def write_json(zf: zipfile.ZipFile, path: str, data: dict) -> None:
    zf.writestr(path, json.dumps(data, indent=2))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "UI2CODE",
        "capabilities": [
            "visual_understanding",
            "ocr_semantics",
            "layout_intelligence",
            "design_system_extraction",
            "component_hierarchy",
            "ai_reasoning",
            "code_generation",
            "responsive_generation",
            "evaluation",
        ],
    })


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(image.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(filepath)

    return jsonify({"redirect_url": f"/editor/{filename}", "filename": filename})


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/editor/<filename>")
def editor(filename):
    return render_template("editor.html", image_file=filename)


@app.route("/api/analyze/<filename>", methods=["GET"])
def analyze_screenshot(filename):
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    framework = request.args.get("framework", Config.DEFAULT_FRAMEWORK)
    styling = request.args.get("styling", Config.DEFAULT_STYLING)

    try:
        result = get_pipeline().analyze(image_path, framework=framework, styling=styling)
        return jsonify(result)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/generate/<filename>", methods=["GET"])
def generate_full_layout(filename):
    """Backward-compatible route used by older UI clients."""
    response = analyze_screenshot(filename)
    if isinstance(response, tuple):
        return response

    data = response.get_json()
    files = data.get("generated_project", {}).get("files", {})
    return jsonify({
        "html": files.get("index.html", files.get("pages/index.js", files.get("App.jsx", ""))),
        "css": files.get("style.css", files.get("styles/globals.css", "")),
        "js": files.get("script.js", ""),
        "analysis": data,
    })


@app.route("/download/<filename>", methods=["GET"])
def download_zip(filename):
    safe_filename = secure_filename(filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    framework = request.args.get("framework", "nextjs")
    styling = request.args.get("styling", Config.DEFAULT_STYLING)

    try:
        result = get_pipeline().analyze(image_path, framework=framework, styling=styling)
        project_files = result.get("generated_project", {}).get("files", {})

        static_files = CodeGenerator(framework="html", styling="css").generate_code(
            result["component_hierarchy"],
            result["design_system"],
            result["layout_intelligence"],
        )

        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("ui2code-generated/README.md", build_project_readme(result))

            for path, content in project_files.items():
                zf.writestr(f"ui2code-generated/project/{path.replace(os.sep, '/')}", content)

            for path, content in static_files.items():
                zf.writestr(f"ui2code-generated/static-html/{path.replace(os.sep, '/')}", content)

            write_json(zf, "ui2code-generated/analysis/full-analysis.json", result)
            write_json(zf, "ui2code-generated/analysis/component-hierarchy.json", result["component_hierarchy"])
            write_json(zf, "ui2code-generated/analysis/design-system.json", result["design_system"])
            write_json(zf, "ui2code-generated/analysis/layout-intelligence.json", result["layout_intelligence"])
            write_json(zf, "ui2code-generated/analysis/ocr-semantics.json", result["ocr_semantics"])
            write_json(zf, "ui2code-generated/analysis/evaluation.json", result["evaluation"])

            extension = os.path.splitext(safe_filename)[1] or ".png"
            zf.write(image_path, f"ui2code-generated/assets/source-screenshot{extension}")

        memory_file.seek(0)
        return send_file(
            memory_file,
            download_name="ui2code-generated-project.zip",
            as_attachment=True,
            mimetype="application/zip",
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
