#!/bin/bash

# Script para configurar servidor Debian 12 para Whisper API com GPU NVIDIA L40
# Execute como root ou com sudo

set -e

echo "🚀 Configurando servidor para Whisper API com GPU NVIDIA L40..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
apt-get update && apt-get upgrade -y

# Instalar dependências básicas
echo "🔧 Instalando dependências básicas..."
apt-get install -y \
    curl \
    wget \
    gnupg \
    lsb-release \
    ca-certificates \
    software-properties-common \
    apt-transport-https

# Instalar Docker
echo "🐳 Instalando Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker instalado com sucesso"
else
    echo "✅ Docker já está instalado"
fi

# Verificar se NVIDIA drivers estão instalados
echo "🎮 Verificando drivers NVIDIA..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ Drivers NVIDIA não encontrados!"
    echo "Por favor, instale os drivers NVIDIA antes de continuar:"
    echo "1. Adicione o repositório NVIDIA:"
    echo "   wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.0-1_all.deb"
    echo "   dpkg -i cuda-keyring_1.0-1_all.deb"
    echo "   apt-get update"
    echo "2. Instale os drivers:"
    echo "   apt-get install -y nvidia-driver-535 nvidia-dkms-535"
    echo "3. Reinicie o sistema e execute este script novamente"
    exit 1
else
    echo "✅ Drivers NVIDIA encontrados"
    nvidia-smi
fi

# Instalar NVIDIA Container Toolkit
echo "🔧 Instalando NVIDIA Container Toolkit..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

apt-get update
apt-get install -y nvidia-container-toolkit

# Configurar Docker para usar NVIDIA runtime
echo "⚙️ Configurando Docker para GPU..."
nvidia-ctk runtime configure --runtime=docker
systemctl restart docker

# Testar configuração GPU
echo "🧪 Testando configuração GPU..."
if docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu22.04 nvidia-smi; then
    echo "✅ GPU configurada com sucesso!"
else
    echo "❌ Erro na configuração da GPU"
    exit 1
fi

# Configurar firewall (opcional)
echo "🔒 Configurando firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 22/tcp
    ufw allow 9005/tcp
    ufw --force enable
    echo "✅ Firewall configurado (portas 22 e 9005 abertas)"
fi

# Criar usuário para aplicação (opcional)
echo "👤 Configurando usuário para aplicação..."
if ! id "whisper" &>/dev/null; then
    useradd -m -s /bin/bash whisper
    usermod -aG docker whisper
    echo "✅ Usuário 'whisper' criado e adicionado ao grupo docker"
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p /opt/whisper-api
mkdir -p /var/log/whisper-api
chown -R whisper:whisper /opt/whisper-api
chown -R whisper:whisper /var/log/whisper-api

echo ""
echo "🎉 Configuração do servidor concluída!"
echo ""
echo "Próximos passos:"
echo "1. Instale o Coolify seguindo a documentação oficial"
echo "2. Configure seu repositório Git com o código da Whisper API"
echo "3. Faça o deploy através do Coolify"
echo ""
echo "Para testar a GPU:"
echo "docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu22.04 nvidia-smi"
echo ""
echo "Informações do sistema:"
echo "- Docker version: $(docker --version)"
echo "- NVIDIA Driver: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits)"
echo "- GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader,nounits)"

