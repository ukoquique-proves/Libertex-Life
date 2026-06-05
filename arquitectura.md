Documentación Técnica: Sistema Automatizado de Gestión de Riesgo y Trading (Libertex-MT5 Bridge)

1. Arquitectura del Sistema

El sistema se compone de tres capas principales:

    Capa de Estrategia e Inversión (Largo Plazo): Módulo de monitoreo de fundamentales (para activos como NVIDIA).

    Capa de Trading Técnico (Corto Plazo): Script ejecutor para operar CFDs en Libertex (Oro, Bitcoin, Divisas).

    Capa de Control de Riesgo (La "Caja Negra" de Seguridad): Código estricto que bloquea la ejecución si se violan los parámetros de pérdida.

[ El Código / Lógica ] 
        │
        ▼ (Vía MQL5 o Python API)
[ Terminal MetaTrader 5 ] ───► [ Servidor Libertex ]


2. Configuración del Entorno y Conectividad

Para poder programar de forma nativa e interactuar con los gráficos que viste en la app, tienes dos caminos principales como desarrollador:
Opción A: Python (Recomendado para análisis de datos)

MetaTrader 5 tiene una librería oficial para Python (MetaTrader5) que permite extraer datos históricos, precios en tiempo real y enviar órdenes de compra/venta.

pip install MetaTrader5 pandas


Opción B: MQL5 (Nativo)

Si se prefiere que el código corra directamente dentro de la plataforma sin dependencias externas, utilizarás MQL5 (un lenguaje de programación muy similar a C++ orientado a objetos).


3. Módulos Críticos a Programar (Tu Blueprint de Código)

Módulo I: El Controlador de Riesgo Matemático (RiskManager)

Este es el módulo más astuto de tu software. Debe ser inmutable; las estrategias pueden cambiar, pero las reglas de riesgo no. El bridge de FastAPI actúa como un **Gatekeeper de Seguridad**, validando cada operación antes de que llegue al broker.

    Regla del 1% al 2%: El código calcula el tamaño de la posición dinámicamente según el balance actual y el stop loss definido.

    Daily Max Drawdown: Si el bot acumula una pérdida del 5% en el día, se activa el cierre masivo de posiciones y se bloquea el trading por 24 horas.


Módulo II: El Gestor de Órdenes (OrderExecutor)

La ejecución de órdenes prioriza la precisión de la gestión de riesgo sobre la velocidad extrema:

- **Control de Desviación (Slippage):** Cada orden incluye el parámetro `deviation: 20`. Esto garantiza que si el precio se desliza más de 2 pips entre el cálculo y la ejecución, MT5 rechazará la orden automáticamente.
- **Política de Ejecución FOK (Fill or Kill):** Se utiliza `mt5.ORDER_FILLING_FOK`. La orden se ejecuta completa al precio solicitado o se cancela, eliminando riesgos de ejecuciones parciales.
- **Latencia Aceptable:** Para estrategias Swing e Intradía, una latencia de 50-150ms introducida por Wine es estadísticamente irrelevante para el R-multiple de la estrategia.

import MetaTrader5 as mt5

def abrir_operacion_cfd(symbol, action, lotes, stop_loss_pips, take_profit_pips):
    # ... (lógica de conexión)
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lotes,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20, # Protección contra Slippage
        "magic": MAGIC_NUMBER,
        "comment": "Bot Automatizado - Estrategia Híbrida",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK, # Fill or Kill para seguridad
    }
    
    result = mt5.order_send(request)
    return result
    
    
Módulo III: Filtro de Noticias y Spread (Filtro Fundamental)

A raíz de lo que hablamos sobre las noticias de Microsoft e IA, tu código debe ser inteligente y no operar a ciegas ante eventos macroeconómicos.

    Evitar "Gaps": Programa un script secundario que consuma un calendario económico (puedes usar web scraping o una API de noticias financieras).

    Regla: Si hay una noticia de alto impacto (tasas de interés de la Fed, reportes de desempleo o ganancias de las Big Tech) en los próximos 30 minutos, el bot tiene prohibido abrir nuevas posiciones en los CFDs afectados para evitar la volatilidad extrema.


4. Fase de Pruebas Obligatoria: Entorno Sandbox (Demo)

Como desarrollador, se que no se sube código a producción sin pasar por un entorno de Staging.

    Conexión Demo: En Libertex, solicita las credenciales para su servidor de MetaTrader en modo Demo.

    Backtesting: Si programas en MQL5, usa el Strategy Tester incorporado para correr tu código con los datos históricos de los últimos 2 años de Bitcoin o el Oro. Mira si tu algoritmo habría sobrevivido a las caídas del mercado.

    Forward Testing: Deja el bot corriendo en la cuenta demo con dinero ficticio durante al menos 2 o 3 semanas. Monitorea los logs en busca de errores de ejecución de órdenes, latencia o cálculos erróneos en el Stop Loss.
    

5. El "Dashboard" del Inversionista Astuto (Tu Toque Personal)

Ya que soy programador, no limitarme a ver los gráficos parpadeantes de la app. Puedo armar un pequeño script local que combine:

    La salud de mi cuenta de trading de corto plazo (Libertex).

    Un portafolio estático donde simule mis compras a largo plazo (acciones reales de NVIDIA, Microsoft, etc.).

De esa manera tendré en una sola pantalla tu "Fondo Seguro" creciendo con el interés compuesto de la tecnología, y mi "Algoritmo de Trading" rascando ganancias diarias en el mercado de CFDs.
