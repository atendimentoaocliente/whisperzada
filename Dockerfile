FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir openai-whisper fastapi uvicorn

WORKDIR /app
COPY ./app.py /app/app.py

EXPOSE 9005

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9005"]
