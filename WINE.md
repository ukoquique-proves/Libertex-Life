# Plan de Instalación: MetaTrader 5 Bridge sobre Wine

Debido a que la librería `MetaTrader5` de Python es exclusiva de entornos Windows, y nos encontramos en un sistema Linux (Debian Bookworm), la alternativa viable para ejecutar el código localmente es utilizar **Wine** (capa de compatibilidad de Windows para Linux).

Este documento detalla los pasos necesarios para instalar Wine, configurar Python para Windows dentro de este entorno, e instalar las dependencias necesarias para ejecutar nuestra API REST (Bridge).

## Requisitos Previos

- Permisos de superusuario (root) para instalar paquetes del sistema.
- Conexión a internet estable para descargar los paquetes y dependencias.

## Fase 1: Instalación de Wine en Debian

1. **Habilitar arquitectura de 32 bits** (recomendado para mayor compatibilidad con Wine):
   ```bash
   dpkg --add-architecture i386
   apt update
   ```

2. **Instalar el paquete base de Wine**:
   ```bash
   apt install -y wine wine32 wine64
   ```

3. **Verificar la instalación**:
   ```bash
   wine --version
   ```

## Fase 2: Instalación de Python (Versión Windows)

1. **Descargar el instalador de Python para Windows** (ej. versión 3.11.9):
   ```bash
   wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
   ```

2. **Instalar Python silenciosamente a través de Wine**:
   ```bash
   wine python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
   ```
   *Nota: `PrependPath=1` asegura que Python y Pip se agreguen a las variables de entorno de Wine.*

## Fase 3: Instalación de Dependencias del Bridge

Una vez que Python para Windows está instalado bajo Wine, instalaremos las librerías necesarias:

1. **Actualizar pip (recomendado)**:
   ```bash
   wine python -m pip install --upgrade pip
   ```

2. **Instalar dependencias del proyecto**:
   Nos posicionamos en el directorio del proyecto y ejecutamos:
   ```bash
   wine python -m pip install MetaTrader5 fastapi uvicorn pydantic
   ```
   *Esto instalará exitosamente la versión de `MetaTrader5` porque se está ejecutando desde el Python emulado de Windows.*

## Fase 4: Ejecución del Bridge API

Para arrancar el servidor FastAPI local, usaremos el mismo comando estándar pero precedido por `wine python`:

```bash
wine python -m uvicorn bridge_app.main:app --host 0.0.0.0 --port 8000
```

## Consideraciones de Ingeniería y Estabilidad

### Latencia vs. Gestión de Riesgo
Aunque ejecutar una API HTTP a través de Wine agrega una ligera capa de latencia (50-150ms), este costo es un **trade-off aceptable** frente a los beneficios de la automatización:
- **Estrategia Swing/Intradía:** La latencia es estadísticamente irrelevante para el R-multiple de la estrategia en marcos temporales de horas o días.
- **Protección de Precio:** El sistema utiliza `deviation: 20` y `ORDER_FILLING_FOK` para garantizar que la orden se ejecute bajo los parámetros de precio deseados o se cancele.
- **Gatekeeper de Riesgo:** La capa FastAPI asegura que ninguna orden llegue al broker sin pasar por el filtro de Drawdown y cálculo de lotaje.

### Estabilidad y Escalabilidad
- **El cuello de botella real:** La estabilidad a largo plazo depende de la persistencia del proceso IPC con la interfaz gráfica de `terminal.exe` bajo Wine.
- **Ruta de Migración:** Si en el futuro se requiere reducir la latencia a cero o mejorar la estabilidad operativa, el diseño desacoplado permite portar el servicio FastAPI de forma nativa a un **Windows Server/VPS** sin modificar la lógica del código.
