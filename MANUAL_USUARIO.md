# Manual de Usuario  
# RSM Primer Orden

Aplicativo interactivo para el diseño, análisis y documentación de experimentos mediante **Metodología de Superficie de Respuesta de Primer Orden**.

---

## 1. Objetivo de la aplicación

La aplicación **RSM Primer Orden** permite construir, analizar e interpretar diseños experimentales de primer orden de manera interactiva.

El sistema está diseñado para apoyar al usuario en:

- Crear diseños factoriales completos \(2^k\).
- Definir factores experimentales y niveles bajo/alto.
- Incluir puntos centrales.
- Registrar respuestas experimentales.
- Cargar datos propios desde Excel o CSV.
- Ajustar un modelo lineal de primer orden.
- Evaluar la significancia global mediante ANOVA.
- Analizar residuos.
- Identificar factores importantes mediante Pareto de efectos.
- Proponer una ruta de ascenso o descenso más pronunciado.
- Generar un reporte gerencial en PDF.
- Descargar respaldo en Excel.

---

## 2. Público objetivo

Esta aplicación está dirigida a:

- Estudiantes de estadística, ingeniería o carreras afines.
- Docentes que enseñan diseño experimental.
- Investigadores que desean explorar una región experimental inicial.
- Usuarios técnicos que necesitan analizar el efecto de varios factores sobre una respuesta.

---

## 3. Alcance metodológico

La aplicación trabaja exclusivamente con modelos de **primer orden**.

Incluye:

- Diseño factorial \(2^k\).
- Puntos centrales.
- Codificación de factores en escala \(-1, 0, +1\).
- Modelo lineal de primer orden.
- ANOVA.
- Diagnóstico de residuos.
- Pareto de efectos.
- Ascenso o descenso más pronunciado.
- Reporte ejecutivo.

No incluye:

- Diseños centrales compuestos.
- Diseños Box-Behnken.
- Modelos cuadráticos.
- Punto estacionario.
- Análisis canónico.
- Ridge analysis.
- Optimización multirespuesta.

---

## 4. Estructura general de la aplicación

La aplicación contiene los siguientes módulos:

```text
Inicio
→ Diseño Experimental
→ Datos Experimentales
→ Modelo Lineal
→ ANOVA
→ Diagnóstico
→ Pareto
→ Ascenso Más Pronunciado
→ Reporte
→ Uso de IA