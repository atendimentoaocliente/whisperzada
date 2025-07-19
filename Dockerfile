FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema (python3.10 e pip já vêm com ubuntu22.04)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Pré-baixar o modelo Whisper large
RUN python3 -c "import whisper; whisper.load_model(\'large\', download_root=\'./whisper_models\')"

# Copiar o restante da aplicação
COPY . .

# Expor a porta 9005
EXPOSE 9005

# Comando para iniciar a aplicação com Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9005", "--timeout-keep-alive", "120", "--timeout-graceful-shutdown", "120"]

