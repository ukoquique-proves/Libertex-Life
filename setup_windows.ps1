# Script de Configuración Automática para Libertex MT5 Bridge (Windows Nativo)

Write-Host "Iniciando configuración nativa del Bridge en Windows..." -ForegroundColor Cyan

# 1. Verificar si Python está instalado
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python no está instalado. Por favor instálalo desde python.org y asegúrate de marcar 'Add to PATH'." -ForegroundColor Red
    exit
}

# 2. Crear entorno virtual
Write-Host "Creando entorno virtual (venv)..." -ForegroundColor Green
python -m venv venv
.\venv\Scripts\activate

# 3. Actualizar pip e instalar dependencias
Write-Host "Instalando dependencias (MetaTrader5, FastAPI, uvicorn)..." -ForegroundColor Green
python -m pip install --upgrade pip
python -m pip install -r bridge_app/requirements.txt

# 4. Crear archivo .env de ejemplo si no existe
if (!(Test-Path .env)) {
    Write-Host "Creando archivo .env de ejemplo..." -ForegroundColor Yellow
    "MT5_ACCOUNT=tu_cuenta`nMT5_PASSWORD=tu_password`nMT5_SERVER=tu_servidor" | Out-File -FilePath .env -Encoding utf8
}

Write-Host "`nConfiguración completada exitosamente." -ForegroundColor Cyan
Write-Host "Para iniciar el Bridge, usa el siguiente comando:" -ForegroundColor Yellow
Write-Host ".\venv\Scripts\python.exe -m uvicorn bridge_app.main:app --host 0.0.0.0 --port 8000"
