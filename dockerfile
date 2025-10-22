FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

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
    libopencv-core-dev \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

RUN git lfs install --skip-repo

EXPOSE 7860

CMD gunicorn run:app --bind 0.0.0.0:$PORT --workers 1 --threads 4
