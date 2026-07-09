# RSM Primer Orden

Aplicativo interactivo desarrollado en **Streamlit** para el análisis de **Diseños Experimentales de Primer Orden** mediante metodología de superficie de respuesta.

El sistema permite diseñar experimentos factoriales completos \(2^k\), registrar o simular respuestas experimentales, ajustar un modelo lineal, evaluar ANOVA, diagnosticar residuos, construir un Pareto de efectos, proponer una ruta de ascenso más pronunciado y generar un reporte ejecutivo en PDF.

---

## Objetivo del aplicativo

Brindar una herramienta práctica, visual e interactiva para aplicar el flujo metodológico de la **Superficie de Respuesta de Primer Orden**, orientada a la toma de decisiones experimentales.

El aplicativo está diseñado para usuarios académicos, técnicos o empresariales que necesiten analizar experimentalmente el efecto de varios factores sobre una variable respuesta.

---

## Alcance metodológico

El aplicativo implementa únicamente métodos de **primer orden**:

- Diseño factorial completo \(2^k\)
- Puntos centrales
- Variables codificadas \(-1, 0, +1\)
- Registro o simulación de variable respuesta
- Modelo lineal de primer orden
- ANOVA global del modelo
- Diagnóstico de residuos
- Pareto de efectos principales
- Ascenso o descenso más pronunciado
- Reporte ejecutivo gerencial en PDF
- Respaldo en Excel

---

## Fuera del alcance

El sistema no implementa métodos de segundo orden, tales como:

- Diseño central compuesto
- Box-Behnken
- Modelos cuadráticos
- Punto estacionario
- Análisis canónico
- Ridge analysis
- Optimización multirespuesta Derringer-Suich

Estas técnicas corresponden a una fase posterior del análisis de superficie de respuesta.

---

## Flujo del aplicativo

```text
Inicio
→ Diseño Experimental
→ Datos Experimentales
→ Modelo Lineal
→ ANOVA
→ Diagnóstico
→ Pareto de Efectos
→ Ascenso Más Pronunciado
→ Reporte Ejecutivo