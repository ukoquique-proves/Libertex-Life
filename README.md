# Proyecto: Sistema Automatizado de Trading con Libertex

Documentación personal para analizar, practicar y eventualmente automatizar operaciones en la plataforma Libertex, combinando trading de corto plazo con inversión a largo plazo.

---

## Posibilidades de Inversión en Libertex

Libertex ofrece dos modalidades distintas dentro de la misma plataforma. No se trata de que una sea buena y la otra mala, sino de para qué sirve cada una y el nivel de riesgo que estás dispuesto a asumir.

### 1. Libertex CFDs — Trading Activo (Corto Plazo)
Basado en **Análisis Técnico**: aprovechar movimientos de precio en horas o días. El sistema utiliza una arquitectura FastAPI para actuar como un **Gatekeeper de Riesgo**, priorizando el control estricto de capital sobre la latencia de ejecución de milisegundos.

- Disponible en: divisas (EUR/USD), oro, petróleo WTI, Bitcoin, Ethereum, índices
- Usa apalancamiento controlado programáticamente
- **Gestión de Riesgo Nativa:** Control de Slippage (Deviation: 20) y ejecución Fill or Kill (FOK).
- Ideal para estrategias Swing e Intradía donde la latencia de 100ms es irrelevante para la esperanza matemática del sistema.

### 2. Libertex Portfolio — Inversión Real (Largo Plazo)
Basado en **Análisis Fundamental**: entender qué empresas dominan el mundo y comprar una parte real de ellas. Compras la acción real, no un CFD.

- Activos disponibles: Apple, NVIDIA, Microsoft, ETFs, etc.
- Eres propietario real (minoritario) de la empresa
- Sin apalancamiento, sin swaps, sin fecha de vencimiento
- Históricamente, la forma más probada de construir riqueza real
- **El contra:** requiere paciencia. Es un juego de acumulación e interés compuesto, no de ganancias inmediatas.

### Estrategia Híbrida Recomendada

Los inversores más astutos no eligen uno solo. Combinan ambos métodos:

| Capital | Modalidad | Objetivo |
|---|---|---|
| 80-90% | Libertex Portfolio | Crecimiento sólido a largo plazo |
| 10% o menos | Libertex CFDs (demo primero) | Aprendizaje activo con riesgo controlado |

El Portfolio es tu fondo serio para el futuro. Los CFDs son el laboratorio donde desarrollas habilidad técnica con capital que puedes permitirte perder mientras aprendes.

---

## Acceso a la Plataforma

- Usuarios dentro del EEA: **libertex.com**
- Usuarios fuera del EEA: **libertex.org**

La cuenta Demo es **pública y gratuita**. No requiere depósito ni academia. Regístrate directamente en el sitio.

> Ver sección 9 de `ADVERTENCIAS.md` para entender las diferencias regulatorias entre ambas versiones.

---

## Ruta de Despliegue Oficial 🏆

Tras evaluar las dificultades técnicas de emulación en entornos Linux (infierno de dependencias con Wine), se ha determinado que la **Alternativa B (Windows Nativo / VPS)** es la **única ruta oficial soportada** para este proyecto.

### **Por qué Windows Nativo?**
1. **Estabilidad Total:** Eliminación de capas de compatibilidad que introducen inestabilidad en la comunicación IPC con MetaTrader 5.
2. **Fiabilidad de Dependencias:** Evita conflictos de arquitectura (amd64/i386) y paquetes rotos en el gestor de paquetes de Linux.
3. **Mantenimiento Simplificado:** La instalación nativa mediante `.\setup_windows.ps1` garantiza un entorno predecible y profesional.

### **Instrucciones de Despliegue**
Consulta la guía detallada en **[WINDOWS_DEPLOY.md](file:///root/LIFE_ACADEMY/Libertex/WINDOWS_DEPLOY.md)** para configurar tu Bridge en un VPS o VM con Windows.

> **Nota sobre Linux:** Los archivos relacionados con Docker y Wine permanecen en el repositorio únicamente para fines de investigación técnica, pero **no se recomiendan ni se soportan** para trading real debido a la inviabilidad de su mantenimiento en sistemas Debian modernos.

---

## Despliegue con Docker (Alternativa A) 🐳

Para aquellos que prefieren mantener su sistema Linux limpio, hemos incluido un `Dockerfile` que aísla todo el entorno (Wine + Python Windows + API).

### Requisitos
- Docker instalado.
- (Opcional) Acceso a un servidor X o VNC si se desea ver la interfaz de MT5.

### Construcción e Inicio
```bash
# Construir la imagen
docker build -t mt5-bridge .

# Correr el contenedor
docker run -d \
  -p 8000:8000 \
  -e MT5_ACCOUNT=tu_cuenta \
  -e MT5_PASSWORD=tu_password \
  -e MT5_SERVER=tu_servidor \
  --name mt5-bridge-app \
  mt5_bridge
```

*Nota: El contenedor utiliza `Xvfb` internamente para satisfacer la dependencia de GUI de la librería MT5.*

---

## Documentos del Proyecto

| Archivo | Contenido |
|---|---|
| `contexto.txt` | Comparativa de métodos de inversión y perfil de riesgo |
| `arquitectura.md` | Diseño técnico del bot de trading (Python / MQL5 / MT5) |
| `ADVERTENCIAS.md` | Riesgos, señales de alerta y recomendaciones críticas |
| `ESTRATEGIA_ENTREVISTA.md` | Guía para la reunión con el promotor de Life Academy |

---

## Estado Actual

- [ ] Registro en cuenta Demo de libertex.org
- [ ] Explorar Libertex Portfolio
- [ ] Configurar entorno Python con librería MetaTrader5
- [ ] Backtesting del algoritmo con datos históricos (2 años)
- [ ] Forward testing en demo (mínimo 2-3 meses)
- [ ] Evaluación de resultados antes de operar con capital real
