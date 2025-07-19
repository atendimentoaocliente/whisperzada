# 🚀 Deploy Rápido no Coolify

## Pré-requisitos

Antes de fazer o deploy, certifique-se de que seu servidor Debian 12 tem:

1. **NVIDIA L40 GPU** com drivers instalados
2. **Docker** com NVIDIA Container Toolkit
3. **Coolify** instalado e funcionando

### ⚡ Configuração Automática do Servidor

Execute este comando no seu servidor Debian 12:

```bash
curl -fsSL https://raw.githubusercontent.com/SEU-USUARIO/whisper-api-coolify/main/setup-server.sh | sudo bash
```

## 🎯 Deploy no Coolify (3 Passos)

### Passo 1: Criar Nova Aplicação

1. Acesse seu Coolify: `http://seu-servidor:8000`
2. Clique em **"New Resource"** → **"Application"**
3. Escolha **"Docker Compose"**

### Passo 2: Configurar Repositório

1. **Repository URL**: `https://github.com/SEU-USUARIO/whisper-api-coolify.git`
2. **Branch**: `main`
3. **Build Pack**: `Docker Compose`

### Passo 3: Configurar Variáveis (Opcional)

Adicione estas variáveis se necessário:

| Variável | Valor | Obrigatório |
|----------|-------|-------------|
| `CUDA_VISIBLE_DEVICES` | `all` | ✅ |
| `NVIDIA_VISIBLE_DEVICES` | `all` | ✅ |
| `NVIDIA_DRIVER_CAPABILITIES` | `compute,utility` | ✅ |

> **Nota**: Essas variáveis já estão configuradas no docker-compose.yml

## ✅ Pronto!

Clique em **"Deploy"** e aguarde. Sua API estará disponível em:

- **URL**: `https://seu-dominio.com` (ou IP:9005)
- **Health Check**: `GET /`
- **Endpoints**:
  - `POST /v1/audio/transcriptions`
  - `POST /v1/audio/translations`
  - `GET /v1/models`

## 🔧 Configuração no N8N

1. **Credentials** → **Create New** → **OpenAI API**
2. **Configurações**:
   - **API Key**: `whisper-api-key-123` (qualquer string)
   - **Organization ID**: deixe em branco
   - **Base URL**: `https://seu-dominio.com`

## 🧪 Teste Rápido

```bash
curl -X POST \
  -H "Authorization: Bearer test-key" \
  -F "file=@audio.mp3" \
  https://seu-dominio.com/v1/audio/transcriptions
```

## 🆘 Problemas?

1. **GPU não detectada**: Execute `nvidia-smi` no servidor
2. **Container não inicia**: Verifique logs no Coolify
3. **Porta ocupada**: Mude a porta no docker-compose.yml

## 📊 Monitoramento

- **Logs**: Disponíveis na interface do Coolify
- **GPU Usage**: `docker exec CONTAINER_ID nvidia-smi`
- **Health**: Endpoint `/` retorna status da API

