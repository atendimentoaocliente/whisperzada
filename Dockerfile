FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && apt-get install -y python3.9 python3.9-distutils python3.9-venv ffmpeg && rm -rf /var/lib/apt/lists/*

# Instalar pip para python3.9
RUN python3.9 -m ensurepip --upgrade
RUN python3.9 -m pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && \
    python3.9 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9005

CMD ["python3.9", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9005", "--timeout-keep-alive", "120", "--timeout-graceful-shutdown", "120"]
