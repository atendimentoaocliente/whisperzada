from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import os

model = whisper.load_model("large")

app = FastAPI()

@app.post("/v1/audio/transcriptions")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    os.remove(tmp_path)
    return {"text": result["text"]}
