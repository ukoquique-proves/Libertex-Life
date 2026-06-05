# CHANGELOG - Libertex MT5 Bridge

Todas las modificaciones técnicas notables en este proyecto serán documentadas en este archivo.

## [1.0.0] - 2026-06-05

### Añadido
- **Pivot Estratégico (Alternativa B)**: Se oficializa el despliegue nativo en Windows/VPS como la única ruta soportada.
- **Automatización Windows**: Creación de [setup_windows.ps1](file:///root/LIFE_ACADEMY/Libertex/setup_windows.ps1) para instalación automática de entornos virtuales y dependencias.
- **Guía de Despliegue Profesional**: Nuevo archivo [WINDOWS_DEPLOY.md](file:///root/LIFE_ACADEMY/Libertex/WINDOWS_DEPLOY.md).
- **Módulo de Trading Completo**: Implementación de lógica de bajo nivel en `bridge_app/mt5_client.py`.
  - Apertura de órdenes de mercado con Stop Loss y Take Profit automáticos.
  - Consulta de estado de cuenta (balance, equidad, margen).
  - Listado de posiciones abiertas e historial de operaciones.
  - Función de pánico `close_all_positions` para cierre masivo.
- **API REST Robusta**: Expansión de `bridge_app/main.py` con FastAPI incluyendo:
  - Endpoint `POST /api/v1/order` con soporte para cálculo de riesgo dinámico (1% por defecto).
  - Endpoints para monitoreo: `/api/v1/account`, `/api/v1/positions`, `/api/v1/history`.
  - Sistema de salud: `/api/v1/status` ahora verifica la conexión activa con el terminal MT5.
- **Capa de Seguridad (Risk Management)**:
  - Implementación de **Daily Drawdown Limit**: Bloqueo automático de trading por 24 horas si las pérdidas del día exceden el 5% del balance.
  - Estructura para **Filtro Fundamental**: Bloqueo preventivo de trading ante noticias de alto impacto.
- **Dockerización (Alternativa A)**: Creación de un `Dockerfile` optimizado que incluye:
  - Wine 64-bit y arquitecturas i386.
  - Servidor X virtual (`Xvfb`) para soporte de GUI de MT5 en entornos headless.
  - Python 3.11 para Windows preconfigurado bajo Wine.
  - Script de entrada `entrypoint.sh` para gestión de procesos.
- **Optimización de Concurrencia**:
  - Implementación de `run_in_threadpool` en todos los endpoints de FastAPI.
  - Conversión de la API a `async` para evitar el bloqueo del event loop por las llamadas síncronas de la librería `MetaTrader5`.
  - Mejora en la estabilidad del servidor bajo carga de peticiones simultáneas.
- **Gestión Avanzada de Órdenes y Riesgo**:
  - Implementación de cálculo de lotaje ultra-preciso basado en `tick_value` y `tick_size` de MT5.
  - Normalización de volumen: Validación estricta contra `volume_min`, `volume_max` y `volume_step` del símbolo para evitar rechazos silenciosos.
  - Filtro de **Spread Máximo**: Bloqueo automático de entradas si el spread excede los 10 pips (configurable).
  - Endpoints para gestión de ciclo de vida: Modificación de SL/TP (`PUT`) y cierre de posición por ticket (`DELETE`).
  - Endpoint de **Dashboard Summary**: Resumen consolidado de salud de cuenta, riesgo activo y estado de drawdown.
- **Refactorización y Estabilidad**:
  - Fijación de versiones en `requirements.txt` para asegurar reproducibilidad en producción.
  - Centralización del `MAGIC_NUMBER` como constante para identificación de órdenes.
  - Documentación del riesgo operativo en el filtro fundamental (Noticias).
- **Optimización de Conexión MT5**:
  - Implementación de `is_connected()` usando `mt5.terminal_info()` para verificar el estado de la conexión.
  - Eliminación de llamadas redundantes a `mt5.initialize()` en el flujo de ejecución de órdenes, reduciendo el overhead y mejorando la estabilidad.
  - Robustez en `close_all_positions`: Añadido guard para evitar crashes (`NoneType error`) si falla la obtención del precio (tick) de un símbolo.
- **Actualización de Infraestructura FastAPI**:
  - Migración del manejo de eventos `startup`/`shutdown` (deprecados) al patrón **Lifespan**.
  - Mejora en la gestión del ciclo de vida de la conexión con MT5, asegurando un cierre limpio de la librería al detener el servidor.
- **Estatismo en el RiskManager**:
  - Eliminación de variables de estado locales para el cálculo de Drawdown.
  - Implementación de cálculo en tiempo real basado en el historial de operaciones cerradas hoy + beneficio flotante actual.
  - El sistema ahora es resiliente a reinicios: si el script falla y se reinicia, el bloqueo por Drawdown se recalcula correctamente desde la fuente de verdad (MT5).
- **Ruta Profesional Windows (Alternativa B)**:
  - Creación de [setup_windows.ps1](file:///root/LIFE_ACADEMY/Libertex/setup_windows.ps1) para automatización de dependencias en Windows/VPS.
  - Documentación detallada de despliegue en [WINDOWS_DEPLOY.md](file:///root/LIFE_ACADEMY/Libertex/WINDOWS_DEPLOY.md).
  - Priorización de esta ruta en el README como la opción recomendada para producción.

### Cambiado
- Estructura de `TradeRequest`: Ahora permite enviar órdenes especificando `risk_percent` o `sl_pips` para que el bot calcule el lotaje óptimo.
- Lógica de Inicialización: Mejora en el manejo de errores durante el login a la cuenta MT5.
- **Filosofía Arquitectónica**: Actualización de la documentación técnica para reflejar que la latencia introducida por Wine (50-150ms) es un trade-off aceptable para estrategias Swing/Intradía, priorizando el control de riesgo (Deviation, FOK, Drawdown) sobre la velocidad HFT.

### Documentación
- Actualización de `TO_DO.md` con checkboxes para seguimiento de tareas completadas y pendientes.
- Referencias técnicas cruzadas en `arquitectura.md` y `README.md`.
