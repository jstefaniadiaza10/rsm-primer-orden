import pandas as pd


def get_ai_tools_df():
    return pd.DataFrame([
        {
            "Herramienta": "ChatGPT - OpenAI",
            "Tipo de uso": "Asistencia técnica y académica",
            "Aplicación en el proyecto": (
                "Apoyo en la estructuración del aplicativo, redacción de documentación, "
                "depuración de errores, organización del flujo metodológico y generación "
                "de fragmentos de código en Python/Streamlit."
            ),
            "Nivel de intervención": "Asistencial, no autónomo"
        }
    ])


def get_ai_disclosure_markdown():
    return """
## Declaración de uso de Inteligencia Artificial

Para el desarrollo de este aplicativo se utilizó asistencia de inteligencia artificial generativa, específicamente **ChatGPT de OpenAI**, como herramienta de apoyo técnico y académico.

El uso de IA se limitó a las siguientes actividades:

- Organización de la estructura del proyecto.
- Apoyo en la redacción técnica y documentación.
- Sugerencias de diseño visual e interfaz.
- Generación y depuración asistida de código en Python y Streamlit.
- Apoyo en la explicación metodológica de los módulos de análisis.
- Estructuración del reporte ejecutivo y del flujo de navegación.

La inteligencia artificial **no sustituyó el criterio académico ni estadístico** del autor.  
Las decisiones metodológicas, validaciones, interpretación de resultados y revisión final fueron responsabilidad del desarrollador del aplicativo.

## Herramientas de IA utilizadas

| Herramienta | Uso principal |
|---|---|
| ChatGPT - OpenAI | Asistencia en programación, documentación, depuración y estructuración metodológica |

## Limitaciones del uso de IA

Los resultados generados por la IA fueron revisados, ajustados y validados antes de incorporarse al aplicativo.  
El sistema final debe ser interpretado como una herramienta académica de apoyo para diseños experimentales de primer orden, no como un sustituto del análisis experto.

## Responsabilidad académica

El autor declara que el uso de inteligencia artificial fue de carácter complementario y transparente, respetando los principios de honestidad académica, trazabilidad y responsabilidad en el desarrollo del proyecto.
"""