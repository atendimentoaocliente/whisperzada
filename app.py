from fastapi import FastAPI, UploadFile, File, Form
import whisper
import tempfile
import os

# Define o diretório onde o modelo será salvo dentro do container
model_dir = os.path.join(os.getcwd(), "whisper_models")

app = FastAPI()

# Variável global para o modelo
model = None

@app.on_event("startup")
async def load_model():
    global model
    # O modelo 'large' é o que você está usando, e o nó OpenAI do n8n pode enviar 'whisper-1'
    # Mantenha 'large' aqui, pois é o modelo que você pré-baixou e quer usar.
    # Se o n8n enviar 'whisper-1', ele será ignorado, e 'large' será usado.
    model = whisper.load_model("large", download_root=model_dir)

@app.post("/v1/audio/transcriptions")
async def transcribe(file: UploadFile = File(...), model_name: str = Form("whisper-1")):
    # O parâmetro model_name é aceito para compatibilidade com a API da OpenAI,
    # mas o modelo 'large' pré-baixado será sempre usado.
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    os.remove(tmp_path)
    return {"text": result["text"]}

# Adicionando um endpoint raiz para compatibilidade e health check
@app.get("/")
async def root():
    return {"message": "Whisper API está no ar!"}


