from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import os

app = FastAPI()

# Variável global para o modelo
model = None

@app.on_event("startup")
async def load_model():
    global model
    model = whisper.load_model("large")

@app.post("/v1/audio/transcriptions")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    os.remove(tmp_path)
    return {"text": result["text"]}
