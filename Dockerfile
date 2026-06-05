# Dockerfile para Libertex MT5 Bridge
# Basado en Debian con Wine y Python para Windows

FROM debian:bookworm-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive
ENV WINEPREFIX=/root/.wine
ENV WINEARCH=win64
ENV DISPLAY=:99

# 1. Instalar dependencias del sistema y Wine
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    wine \
    wine32 \
    wine64 \
    wget \
    ca-certificates \
    xvfb \
    procps \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Descargar e instalar Python para Windows
RUN wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe -O /tmp/python-installer.exe && \
    xvfb-run wine /tmp/python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 && \
    rm /tmp/python-installer.exe

# 3. Configurar directorio de trabajo
WORKDIR /app

# 4. Copiar código del proyecto
COPY . .

# 5. Instalar dependencias de Python bajo Wine
RUN xvfb-run wine python -m pip install --upgrade pip && \
    xvfb-run wine python -m pip install -r bridge_app/requirements.txt

# 6. Exponer puerto de la API
EXPOSE 8000

# 7. Script de inicio para manejar Xvfb y FastAPI
RUN echo '#!/bin/bash\n\
# Iniciar servidor X virtual para la GUI de MT5\n\
Xvfb :99 -screen 0 1024x768x16 &\n\
\n\
echo "Iniciando Bridge API bajo Wine..."\n\
wine python -m uvicorn bridge_app.main:app --host 0.0.0.0 --port 8000\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
