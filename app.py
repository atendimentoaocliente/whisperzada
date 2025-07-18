from fastapi import FastAPI, UploadFile, File
import whisper
import torch

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("large").to(device)

@app.post("/v1/audio/transcriptions")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = model.transcribe("temp.wav")
    return {
        "text": result["text"],
        "language": result.get("language"),
        "segments": result.get("segments", [])
    }
