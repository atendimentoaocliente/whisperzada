# Whisper API com GPU para Coolify

## Como funciona

- API FastAPI que recebe áudio e retorna texto transcrito usando Whisper da OpenAI
- Usa GPU via Docker NVIDIA runtime
- Roda na porta 9005

## Deploy no Coolify

- Configure app para usar Docker Compose
- Aponte para este repositório GitHub
- Configure porta 9005 externa e interna
- Habilite GPU (runtime NVIDIA)

## Teste local

```bash
docker build -t whisper-api .
docker run --gpus all -p 9005:9005 whisper-api
