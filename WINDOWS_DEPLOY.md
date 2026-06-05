# Guía de Despliegue: Alternativa B (Ruta Profesional Windows)

Esta es la configuración recomendada para entornos de **Trading Real** o **Forward Testing** de largo plazo. Utilizar una máquina virtual (VM) o un VPS con Windows garantiza la máxima estabilidad operativa del Bridge.

## Ventajas de la Ruta Profesional
- **Estabilidad Nativa:** Sin capas de emulación (Wine). La comunicación IPC entre la librería de Python y `terminal.exe` es directa y robusta.
- **Baja Latencia:** Eliminación de los milisegundos de procesamiento de la capa de compatibilidad.
- **Facilidad de Debugging:** Puedes ver la interfaz de MetaTrader 5 directamente para monitorear órdenes, logs del terminal y conexión al servidor de Libertex.

## Pasos para la Implementación

### 1. Preparación del Entorno (Windows VM/VPS)
- Asegúrate de tener Windows Server 2019/2022 o Windows 10/11 instalado.
- Instala el terminal de escritorio de **MetaTrader 5** proporcionado por Libertex.
- Inicia sesión en tu cuenta Demo/Real y asegúrate de que el terminal esté conectado (icono verde en la esquina inferior derecha).

### 2. Instalación del Bridge
Copia la carpeta del proyecto a tu máquina Windows y ejecuta el script de automatización que hemos preparado:

```powershell
# Abre PowerShell en la carpeta del proyecto y ejecuta:
.\setup_windows.ps1
```

Este script creará un entorno virtual e instalará todas las dependencias necesarias.

### 3. Configuración de Variables de Entorno
Edita el archivo `.env` creado en la raíz del proyecto con tus credenciales:
```env
MT5_ACCOUNT=12345678
MT5_PASSWORD=tu_contraseña_segura
MT5_SERVER=Libertex-Demo
```

### 4. Ejecución del Servicio
Inicia el servidor FastAPI:
```powershell
.\venv\Scripts\python.exe -m uvicorn bridge_app.main:app --host 0.0.0.0 --port 8000
```

### 5. Conexión desde Linux (Tu App Principal)
Ahora tu aplicación principal (Node.js, Python o UI) que corre en Linux puede comunicarse con el Bridge mediante peticiones HTTP estándar:

```javascript
// Ejemplo desde Node.js
const response = await fetch('http://IP_DE_TU_VM_WINDOWS:8000/api/v1/price/GOLD');
const price = await response.json();
```

## Recomendaciones de Mantenimiento
- **Auto-reinicio:** Configura el script de ejecución como una tarea programada en Windows para que se inicie automáticamente al arrancar el sistema.
- **Monitoreo Visual:** Mantén la ventana de MetaTrader 5 minimizada pero abierta; la librería la necesita para funcionar.
- **Firewall:** Asegúrate de abrir el puerto 8000 en el Firewall de Windows para permitir las peticiones entrantes desde tu servidor Linux.
