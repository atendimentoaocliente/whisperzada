# Deploy no Coolify - Whisper API

## Pré-requisitos

1. **Servidor Debian 12 com:**
   - Docker instalado
   - NVIDIA Container Toolkit instalado
   - GPU NVIDIA L40 configurada
   - Coolify instalado e configurado

2. **Repositório Git:**
   - Código da aplicação em um repositório Git (GitHub, GitLab, etc.)

## Passos para Deploy

### 1. Preparação do Servidor

Certifique-se de que o NVIDIA Container Toolkit está instalado:

```bash
# Instalar NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Testar se GPU está acessível
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### 2. Deploy via Coolify

#### Opção 1: Docker Compose (Recomendado)

1. **Criar Nova Aplicação no Coolify:**
   - Acesse sua instância do Coolify
   - Clique em "New Resource" → "Application"
   - Escolha "Docker Compose"

2. **Configurar Repositório:**
   - Conecte seu repositório Git
   - Branch: `main` ou `master`
   - Build Pack: `Docker Compose`

3. **Configurar Docker Compose:**
   - O Coolify usará automaticamente o arquivo `docker-compose.yml`
   - Certifique-se de que o arquivo está na raiz do repositório

4. **Variáveis de Ambiente:**
   - Adicione as seguintes variáveis no Coolify:
     - `CUDA_VISIBLE_DEVICES=all`
     - `NVIDIA_VISIBLE_DEVICES=all`
     - `NVIDIA_DRIVER_CAPABILITIES=compute,utility`

5. **Deploy:**
   - Clique em "Deploy"
   - Aguarde o build e deploy

#### Opção 2: Dockerfile

1. **Criar Nova Aplicação:**
   - New Resource → Application
   - Escolha "Dockerfile"

2. **Configurações:**
   - Repository: seu repositório Git
   - Build Pack: Dockerfile
   - Port: 9005

3. **Configurações Avançadas:**
   - Em "Environment Variables", adicione:
     - `CUDA_VISIBLE_DEVICES=all`
     - `NVIDIA_VISIBLE_DEVICES=all`
     - `NVIDIA_DRIVER_CAPABILITIES=compute,utility`

4. **Deploy:**
   - Clique em "Deploy"

### 3. Configurações Específicas para GPU

No Coolify, você pode precisar adicionar configurações específicas para GPU:

1. **Docker Daemon Configuration:**
   Certifique-se de que o Docker daemon está configurado para usar o NVIDIA runtime:

```json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

2. **Verificar Logs:**
   - Monitore os logs no Coolify para verificar se a GPU está sendo detectada
   - Procure por mensagens como "CUDA is available" nos logs

### 4. Configuração de Domínio

1. **Adicionar Domínio:**
   - No Coolify, vá para a aplicação
   - Adicione seu domínio personalizado
   - Configure SSL automaticamente

2. **Configurar N8N:**
   - Base URL: `https://seu-dominio.com`
   - API Key: qualquer string não vazia
   - Organization ID: deixe em branco

### 5. Monitoramento

1. **Health Check:**
   - O Coolify monitorará automaticamente a saúde da aplicação
   - Endpoint: `GET /`

2. **Logs:**
   - Acesse os logs através da interface do Coolify
   - Monitore o uso da GPU através dos logs da aplicação

### 6. Atualizações

Para atualizar a aplicação:

1. **Push para Git:**
   - Faça push das alterações para o repositório
   - O Coolify pode ser configurado para auto-deploy

2. **Deploy Manual:**
   - Clique em "Deploy" no Coolify para fazer deploy manual

## Troubleshooting

### GPU não detectada:
- Verifique se o NVIDIA Container Toolkit está instalado
- Confirme que o Docker daemon está configurado corretamente
- Teste com: `docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi`

### Aplicação não inicia:
- Verifique os logs no Coolify
- Confirme se todas as dependências estão instaladas
- Verifique se a porta 9005 está livre

### Problemas de memória:
- A GPU L40 tem 48GB de VRAM
- Monitore o uso de memória nos logs
- Considere usar modelos menores se necessário

## Configuração Final no N8N

Após o deploy bem-sucedido:

1. **Base URL:** `https://seu-dominio.com`
2. **API Key:** qualquer string (ex: `whisper-api-key-123`)
3. **Organization ID:** deixe em branco

A API estará disponível nos endpoints:
- `POST /v1/audio/transcriptions`
- `POST /v1/audio/translations`
- `GET /v1/models`

