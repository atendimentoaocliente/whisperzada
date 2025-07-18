import whisper
from fastapi import FastAPI, UploadFile, File
import tempfile

app = FastAPI()

model = whisper.load_model("large", device="cuda")

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        contents = await audio.read()
        tmp.write(contents)
        tmp.flush()

        result = model.transcribe(tmp.name)

    return {"text": result["text"]}
