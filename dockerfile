# Dockerfile para Render - Flask + TensorFlow (CPU)
FROM python:3.11-slim

# Evita prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 🔧 Instala dependencias del sistema necesarias para TensorFlow, OpenCV, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    git \
    git-lfs \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    libglvnd0 \
    libglx0 \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copia todos los archivos del proyecto al contenedor
COPY . /app

# 🧰 Actualiza pip e instala dependencias Python
RUN python -m pip install --upgrade pip setuptools wheel

# Instala dependencias de tu proyecto
RUN pip install -r requirements.txt

# Configura Git LFS (si lo usas)
RUN git lfs install --skip-repo

# Expone el puerto (Render lo sobreescribirá automáticamente)
EXPOSE 7860

# Comando para iniciar la aplicación con Gunicorn
# Usa ${PORT:-7860} para fallback si PORT no está definido
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:${PORT:-7860}", "--workers", "1", "--threads", "4"]
