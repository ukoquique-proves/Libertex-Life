# ⚠️ ADVERTENCIAS CRÍTICAS - Trading con CFDs y Libertex

## 1. Riesgo Financiero Real

Los CFDs (Contratos por Diferencia) son instrumentos extremadamente volátiles y de alto riesgo. 

**Estadística crucial:** Entre el 70-80% de las personas que operan CFDs pierden su capital invertido.

Esto no es una exageración ni un descargo de responsabilidad legal vacío. Es la realidad demostrada del mercado de CFDs para traders minoristas.

## 2. El Apalancamiento es un Arma de Doble Filo

Aunque el código propuesto en este proyecto incluye controles de riesgo (stop loss automático, límite del 1-2% por operación), el apalancamiento puede liquidar tu cuenta más rápido de lo que cualquier algoritmo pueda reaccionar.

**Situaciones de alto riesgo:**
- Eventos de alta volatilidad (noticias macroeconómicas inesperadas)
- Gaps de mercado (el precio "salta" sin pasar por los niveles intermedios)
- Fines de semana y horarios de baja liquidez
- Eventos del tipo "cisne negro" (crashes inesperados del mercado)

En estas situaciones, tu stop loss puede no ejecutarse al precio esperado, resultando en pérdidas mucho mayores a las calculadas.

## 3. La Automatización NO Elimina el Riesgo

Tener un bot bien programado no te convierte automáticamente en un inversionista exitoso.

**Realidades del trading algorítmico:**
- Los algoritmos profesionales requieren años de desarrollo y ajuste continuo
- El backtesting con datos históricos no garantiza resultados futuros
- Los mercados cambian constantemente (lo que funcionó ayer puede fallar mañana)
- Se necesita capital significativo para absorber las pérdidas inevitables durante el proceso de aprendizaje
- Incluso los fondos de cobertura profesionales con equipos de PhD pierden dinero regularmente

## 4. Recomendaciones de Gestión de Capital

### Estrategia Híbrida Recomendada:

**80-90% del capital:** Inversiones a largo plazo en activos reales
- Acciones de empresas sólidas (Apple, Microsoft, NVIDIA, etc.)
- ETFs diversificados
- Fondos indexados
- Bonos o instrumentos de renta fija

**10% o menos:** Trading activo / experimentación con CFDs
- Solo capital que puedas permitirte perder completamente
- Considéralo como "matrícula" para aprender trading
- Nunca aumentes este porcentaje, sin importar los resultados iniciales

## 5. Proceso Obligatorio ANTES de Usar Dinero Real

### Paso 1: Cuenta Demo (Mínimo 3-6 meses)
- Practica con dinero ficticio en la cuenta demo de Libertex
- Registra todas tus operaciones y resultados
- Analiza tus errores sin consecuencias financieras

### Paso 2: Backtesting Exhaustivo
- Prueba tu estrategia con al menos 2 años de datos históricos
- Verifica cómo habría funcionado durante crisis de mercado (2020, 2022)
- Asegúrate de que el sistema sobrevive períodos de alta volatilidad

### Paso 3: Forward Testing
- Deja el bot corriendo en demo durante semanas
- Monitorea errores de ejecución, latencia, cálculos incorrectos
- Verifica que los stop loss se ejecuten correctamente

### Paso 4: Capital Mínimo Real
- Si decides pasar a real, comienza con el mínimo absoluto
- Nunca con dinero que necesites para gastos esenciales
- Nunca con dinero prestado o apalancamiento externo al broker

## 6. Señales de Alerta - Cuándo DETENERSE

**Detén INMEDIATAMENTE las operaciones si:**
- Has perdido el 20% de tu capital de trading en un mes
- Te encuentras aumentando el tamaño de las posiciones para "recuperar" pérdidas
- Estás operando por emoción en lugar de seguir tu estrategia
- No puedes dormir bien pensando en tus posiciones abiertas
- Estás considerando usar dinero de ahorros o emergencias
- Has dejado de usar stop loss "solo esta vez"

## 7. Alternativas Más Seguras

Antes de arriesgar capital en CFDs, considera:

1. **Inversión pasiva en índices:** Históricamente, el S&P 500 ha dado retornos del 10% anual promedio
2. **Dollar-cost averaging:** Invertir cantidades fijas regularmente reduce el riesgo de timing
3. **ETFs diversificados:** Exposición a múltiples sectores con menor riesgo
4. **Fondos de inversión gestionados:** Profesionales gestionan tu dinero por una comisión

## 8. Disclaimer Legal

Este proyecto es únicamente para fines educativos y de experimentación técnica. 

**No constituye:**
- Asesoría financiera profesional
- Recomendación de inversión
- Garantía de resultados
- Invitación a operar con dinero real

**Consulta siempre con un asesor financiero certificado antes de tomar decisiones de inversión.**

---

## Resumen Final

El mejor código del mundo no puede eliminar el riesgo inherente del trading con CFDs. La programación puede ayudarte a automatizar y gestionar el riesgo, pero no puede predecir el futuro ni garantizar ganancias.

**La estrategia más astuta sigue siendo:** invertir la mayoría de tu capital en activos reales a largo plazo y solo experimentar con una fracción que puedas perder completamente.


## 9. Diferencias Regulatorias: EEA vs. Resto del Mundo

Si operas desde fuera de la Unión Europea (a través de libertex.org), no estás protegido por la regulación de la **ESMA** (Autoridad Europea de Valores y Mercados). Esto tiene consecuencias reales:

- **Apalancamiento sin límite regulado:** En el EEA está limitado a 30:1 en divisas y 2:1 en cripto. Fuera pueden ofrecerte 200:1, 500:1 o más. Más apalancamiento = más riesgo de liquidación total.
- **Sin protección de saldo negativo:** En el EEA es ilegal que pierdas más de lo que depositaste. Fuera del EEA puedes quedar con saldo negativo, es decir, debiéndole dinero al broker.
- **Bonos de depósito como gancho:** Prohibidos en el EEA por ser manipuladores. Fuera se usan frecuentemente para atraer clientes con condiciones que parecen ventajosas pero aumentan la exposición al riesgo.

Lo que el promotor puede presentarte como "ventajas" (más apalancamiento, bonos de bienvenida) son exactamente las características que la regulación europea eliminó para proteger al trader minorista. No son beneficios, son riesgos adicionales.
