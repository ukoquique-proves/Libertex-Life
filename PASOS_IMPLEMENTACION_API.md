# Plan de Implementación: API Bridge (Libertex - MetaTrader 5)

Este documento detalla los pasos a seguir para implementar la estrategia de conexión recomendada (Opción 1: El puente de MetaTrader), evitando el web scraping frágil y asegurando una conexión estable.

## Fase 1: Obtención de Credenciales

- [ ] Iniciar sesión en la cuenta Demo de Libertex (libertex.org).
- [ ] Navegar a la sección de Configuración de la cuenta.
- [ ] Buscar el apartado de "Plataformas de Trading" (Trading Platforms).
- [ ] Generar y copiar el **número de cuenta** de MetaTrader.
- [ ] Generar y copiar la **contraseña** de MetaTrader.
- [ ] Identificar y copiar el **servidor** asignado (ej. `Libertex-Demo`).

## Fase 2: Configuración del Entorno Python (El Bridge)

- [ ] Crear un directorio dedicado para el Bridge (ej. `mt5-bridge`).
- [ ] Inicializar un entorno virtual de Python (`python3 -m venv venv` y `source venv/bin/activate`).
- [ ] Instalar la librería oficial de MetaTrader: `pip install MetaTrader5`.
- [ ] Instalar un framework para la API REST local (ej. FastAPI): `pip install fastapi uvicorn`.

## Fase 3: Desarrollo del Script de Conexión (Backend)

- [ ] Crear un archivo principal (ej. `bridge.py`).
- [ ] Importar `MetaTrader5` y configurar la función de inicialización `mt5.initialize()`.
- [ ] Implementar el login con las credenciales obtenidas en la Fase 1 usando `mt5.login()`.
- [ ] Validar que la conexión sea exitosa y manejar posibles errores de autenticación.

## Fase 4: Creación de la API REST Local

- [ ] Configurar el servidor local con FastAPI/Flask.
- [ ] Crear endpoint GET para consultar precios en tiempo real de un activo (ej. `/api/v1/price/{symbol}`).
- [ ] Crear endpoint POST para abrir órdenes de mercado (Compra/Venta) recibiendo volumen, símbolo, Stop Loss y Take Profit.
- [ ] Crear endpoint POST/PUT para gestionar/modificar una orden existente.
- [ ] Crear endpoint GET para verificar el estado de la cuenta (balance, margen libre).

## Fase 5: Conexión con la Aplicación Principal (Node.js u otro)

- [ ] En la aplicación principal, configurar un cliente HTTP (ej. `axios` o `fetch`).
- [ ] Desarrollar los servicios/controladores para enviar peticiones a la API local del Bridge (ej. `http://localhost:8000/api/v1/...`).
- [ ] Implementar la lógica de envío de órdenes desde la UI o lógica core ("Comprar Oro") hacia el Bridge.
- [ ] Manejar las respuestas del Bridge (confirmación de orden ejecutada, errores, rechazos).

## Fase 6: Pruebas y Validación (Entorno Demo)

- [ ] Ejecutar el Bridge de Python en segundo plano (`uvicorn bridge:app --reload`).
- [ ] Iniciar la aplicación principal.
- [ ] Realizar solicitudes de consulta de precios y validar contra la plataforma de Libertex/MT5.
- [ ] Ejecutar una orden de prueba (ej. comprar un lote mínimo de EUR/USD o Oro) desde la aplicación principal.
- [ ] Verificar en la interfaz de MetaTrader/Libertex que la orden se abrió correctamente con el Stop Loss y Take Profit asignados.
- [ ] Verificar el manejo de errores (ej. enviar una orden sin fondos suficientes, símbolo incorrecto).
