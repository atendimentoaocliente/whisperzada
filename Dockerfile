FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3.9 python3.9-pip ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3.9 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && \
    pip3.9 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9005

CMD ["python3.9", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9005"]
