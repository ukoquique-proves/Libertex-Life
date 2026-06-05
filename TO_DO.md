# TO-DO: Continuar Implementación del Bridge (Libertex - MT5)

## Estado Actual
- [x] **Código Base Creado**: Estructura del backend en Python (FastAPI + MetaTrader5) en `bridge_app/`.
- [x] **Implementación de Lógica de Trading**: Endpoints para órdenes, posiciones e historial.
- [x] **Gestión de Riesgo**: Implementación de RiskManager (1% por operación) y Daily Drawdown (5%).
- [x] **Estrategia Final Definida**: Se descarta la emulación en Linux. El despliegue será **Windows Nativo** para garantizar estabilidad.
- [ ] **Despliegue Final**: Mover la carpeta a un VPS/VM Windows y ejecutar `.\setup_windows.ps1`.

## Tareas Completadas ✅
- [x] Crear endpoint `GET /api/v1/account` para estado de cuenta.
- [x] Crear endpoint `GET /api/v1/positions` para ver operaciones abiertas.
- [x] Crear endpoint `GET /api/v1/history` para historial de trading.
- [x] Crear endpoint `POST /api/v1/order` con cálculo automático de lotaje y riesgo.
- [x] Implementar función de pánico `close_all_positions` ante drawdown crítico.
- [x] Implementar bloqueo de trading por 24h tras alcanzar límite de pérdida diaria.
- [x] **Pivot Estratégico**: Oficializar la Alternativa B (Windows) como la ruta única de producción.
- [x] Crear script de automatización `setup_windows.ps1` y guía `WINDOWS_DEPLOY.md`.
- [x] Desestimar oficialmente la ruta Linux/Wine por inviabilidad técnica de dependencias.

## Próximos Pasos (En orden) 🚀

### 1. Reparar e instalar paquetes interrumpidos
Como la actualización de `apt` se canceló a la mitad, el sistema podría tener paquetes a medio desempaquetar. Al regresar, lo primero que se debe hacer es reparar la instalación e instalar Wine:
```bash
dpkg --configure -a
apt --fix-broken install
apt upgrade -y
apt install -y wine wine32 wine64
```

### 2. Instalar Python para Windows (sobre Wine)
Descargar el instalador y ejecutarlo a través de Wine para que se registre correctamente:
```bash
wget https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
wine python-3.11.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
```

### 3. Instalar Dependencias del Proyecto
Usar el `pip` del Python instalado en Wine para agregar las librerías necesarias para el Bridge:
```bash
wine python -m pip install MetaTrader5 fastapi uvicorn pydantic
```

### 4. Conseguir Credenciales Demo
- [ ] Ir a [libertex.org](https://libertex.org) y buscar la sección de Plataformas (MetaTrader).
- [ ] Apuntar: **Número de Cuenta**, **Contraseña**, y **Servidor**.
- [ ] Configurar variables de entorno (`MT5_ACCOUNT`, `MT5_PASSWORD`, `MT5_SERVER`).

### 5. Iniciar la API Local
```bash
wine python -m uvicorn bridge_app.main:app --host 0.0.0.0 --port 8000
```
- [ ] Verificar conexión desde `http://localhost:8000/docs`.
