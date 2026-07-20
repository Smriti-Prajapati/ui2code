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

# CORS — allow Next.js frontend (localhost dev + Vercel production)
_allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv("FRONTEND_URL", ""),          # e.g. https://ui2code.vercel.app
    os.getenv("FRONTEND_URL_ALT", ""),      # extra alias if needed
]
CORS(app, origins=[o for o in _allowed_origins if o], supports_credentials=True)

pipeline: UI2CodePipeline | None = None


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

Generated from a UI screenshot using visual understanding, OCR, layout intelligence,
design-system extraction, hierarchy reasoning, and code generation.

## Source
- Screenshot: {image.get("filename", "uploaded image")}
- Size: {image.get("width", "-")}x{image.get("height", "-")}
- Components detected: {result.get("visual_understanding", {}).get("component_count", 0)}
- Overall score: {evaluation.get("overall_score", 0):.2f}

## Run
```bash
npm install && npm run dev
```

## Files
{chr(10).join(f"- `{p}`" for p in sorted(files))}
"""


def write_json(zf: zipfile.ZipFile, path: str, data: dict) -> None:
    zf.writestr(path, json.dumps(data, indent=2))


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    # Flask fallback UI (kept for backward compat)
    try:
        return render_template("index.html")
    except Exception:
        return jsonify({"status": "ok", "message": "ui2code API — use the Next.js frontend"})


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "ui2code",
        "version": "2.0.0",
        "capabilities": [
            "visual_understanding", "ocr_semantics", "layout_intelligence",
            "design_system_extraction", "component_hierarchy", "ai_reasoning",
            "code_generation", "responsive_generation", "evaluation",
        ],
    })


@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    image = request.files["image"]
    if not image.filename:
        return jsonify({"error": "No selected file"}), 400
    if not allowed_file(image.filename):
        return jsonify({"error": "Unsupported file type. Use PNG, JPG, or WEBP."}), 400

    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(filepath)

    return jsonify({"redirect_url": f"/editor/{filename}", "filename": filename})


@app.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/editor/<filename>")
def editor(filename: str):
    try:
        return render_template("editor.html", image_file=filename)
    except Exception:
        return jsonify({"redirect": f"/studio/{filename}"}), 302


@app.route("/api/analyze/<path:filename>", methods=["GET"])
def analyze_screenshot(filename: str):
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


@app.route("/download/<path:filename>", methods=["GET"])
def download_zip(filename: str):
    safe = secure_filename(filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], safe)
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    framework = request.args.get("framework", "nextjs")
    styling = request.args.get("styling", Config.DEFAULT_STYLING)

    try:
        result = get_pipeline().analyze(image_path, framework=framework, styling=styling)
        project_files = result.get("generated_project", {}).get("files", {})
        static_files = CodeGenerator(framework="html", styling="css").generate_code(
            result["component_hierarchy"], result["design_system"], result["layout_intelligence"],
        )

        buf = BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
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
            ext = os.path.splitext(safe)[1] or ".png"
            zf.write(image_path, f"ui2code-generated/assets/source-screenshot{ext}")

        buf.seek(0)
        return send_file(buf, download_name="ui2code-generated-project.zip",
                         as_attachment=True, mimetype="application/zip")
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
