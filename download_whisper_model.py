import whisper
import os

# Define o diretório onde o modelo será salvo dentro do container
model_dir = os.path.join(os.getcwd(), "whisper_models")
os.makedirs(model_dir, exist_ok=True)

# Baixa o modelo 'large' para o diretório especificado
whisper._download("large", model_dir)


