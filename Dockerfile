# ── Hugging Face Spaces / Railway / Fly.io compatible Dockerfile ──────────────
# Uses slim requirements — no PyTorch, no heavy ML models
# RAM usage: ~700MB (fits HF Spaces free tier)

FROM python:3.11-slim

# System deps for OpenCV + EasyOCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (layer cache)
COPY backend/requirements-slim.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Create upload + output dirs
RUN mkdir -p uploads output model dataset

# HF Spaces runs as non-root user 1000
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

EXPOSE 7860

# HF Spaces expects port 7860
ENV PORT=7860
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

CMD ["python", "app.py"]
