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
---

## Declaración de uso de Inteligencia Artificial

Para el desarrollo de este aplicativo se utilizó asistencia de inteligencia artificial generativa, específicamente **ChatGPT de OpenAI**, como herramienta de apoyo técnico y académico.

El uso de IA se aplicó en:

- Organización de la estructura del proyecto.
- Apoyo en la redacción técnica y documentación.
- Sugerencias de diseño visual e interfaz.
- Generación y depuración asistida de código en Python y Streamlit.
- Apoyo en la explicación metodológica de los módulos de análisis.
- Estructuración del reporte ejecutivo y del flujo de navegación.

La inteligencia artificial no sustituyó el criterio académico ni estadístico del autor. Las decisiones metodológicas, validaciones, interpretación de resultados y revisión final fueron responsabilidad del desarrollador del aplicativo.

### Herramientas utilizadas

| Herramienta | Uso principal |
|---|---|
| ChatGPT - OpenAI | Asistencia en programación, documentación, depuración y estructuración metodológica |

El uso de IA fue de carácter complementario y transparente, respetando los principios de honestidad académica, trazabilidad y responsabilidad académica.

## Manual de usuario

El proyecto incluye un manual completo de uso en el archivo:

[MANUAL_USUARIO.md](MANUAL_USUARIO.md)

## Datos de prueba

El repositorio incluye un archivo de datos de prueba para ejecutar el flujo completo del aplicativo:

```text
data/datos_prueba_cacao.csv