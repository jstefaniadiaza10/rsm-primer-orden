import pandas as pd

from utils.design_generator import generate_first_order_design, create_factor_summary
from utils.simulator import simulate_first_order_response


EXAMPLE_CASES = {
    "cacao_tostado": {
        "title": "Tostado de cacao Nacional",
        "description": (
            "Ejemplo orientado a optimizar el tostado de cacao ecuatoriano. "
            "Se busca mejorar el puntaje sensorial mediante temperatura, tiempo y humedad inicial."
        ),
        "response_name": "Puntaje sensorial",
        "response_units": "puntos",
        "optimization_goal": "Maximizar",
        "factors": [
            {"name": "Temperatura_C", "low": 120.0, "high": 140.0},
            {"name": "Tiempo_min", "low": 20.0, "high": 40.0},
            {"name": "Humedad_inicial_pct", "low": 6.0, "high": 10.0},
        ],
        "center_points": 3,
        "randomize": True,
        "seed": 101,
        "intercept": 84.0,
        "coefficients": {
            "Temperatura_C": 2.8,
            "Tiempo_min": 1.6,
            "Humedad_inicial_pct": -1.2,
        },
        "noise_sd": 0.75,
    },

    "secado_granos": {
        "title": "Secado de granos",
        "description": (
            "Ejemplo de reducción de humedad final en un proceso de secado. "
            "El objetivo es encontrar condiciones que reduzcan la humedad final."
        ),
        "response_name": "Humedad final",
        "response_units": "%",
        "optimization_goal": "Minimizar",
        "factors": [
            {"name": "Temperatura_C", "low": 45.0, "high": 65.0},
            {"name": "Tiempo_min", "low": 60.0, "high": 120.0},
            {"name": "Velocidad_aire_m_s", "low": 1.0, "high": 3.0},
        ],
        "center_points": 3,
        "randomize": True,
        "seed": 202,
        "intercept": 12.5,
        "coefficients": {
            "Temperatura_C": -1.8,
            "Tiempo_min": -2.2,
            "Velocidad_aire_m_s": -0.9,
        },
        "noise_sd": 0.45,
    },

    "rendimiento_industrial": {
        "title": "Rendimiento de proceso industrial",
        "description": (
            "Ejemplo aplicado a un proceso industrial donde se desea maximizar "
            "el rendimiento a partir de presión, temperatura y velocidad."
        ),
        "response_name": "Rendimiento",
        "response_units": "%",
        "optimization_goal": "Maximizar",
        "factors": [
            {"name": "Presion_bar", "low": 2.0, "high": 5.0},
            {"name": "Temperatura_C", "low": 80.0, "high": 110.0},
            {"name": "Velocidad_rpm", "low": 300.0, "high": 600.0},
        ],
        "center_points": 3,
        "randomize": True,
        "seed": 303,
        "intercept": 72.0,
        "coefficients": {
            "Presion_bar": 1.9,
            "Temperatura_C": 2.4,
            "Velocidad_rpm": 1.1,
        },
        "noise_sd": 0.9,
    },

    "formulacion_alimento": {
        "title": "Formulación de alimento",
        "description": (
            "Ejemplo de formulación donde se analiza el efecto de ingredientes "
            "y temperatura sobre la aceptabilidad del producto."
        ),
        "response_name": "Aceptabilidad",
        "response_units": "puntos",
        "optimization_goal": "Maximizar",
        "factors": [
            {"name": "Ingrediente_A_pct", "low": 10.0, "high": 20.0},
            {"name": "Ingrediente_B_pct", "low": 5.0, "high": 15.0},
            {"name": "Temperatura_C", "low": 60.0, "high": 80.0},
        ],
        "center_points": 3,
        "randomize": True,
        "seed": 404,
        "intercept": 78.0,
        "coefficients": {
            "Ingrediente_A_pct": 1.5,
            "Ingrediente_B_pct": -0.8,
            "Temperatura_C": 2.1,
        },
        "noise_sd": 0.7,
    },
}


def get_example_options():
    return list(EXAMPLE_CASES.keys())


def get_example_case(example_key):
    if example_key not in EXAMPLE_CASES:
        raise ValueError("El ejemplo seleccionado no existe.")
    return EXAMPLE_CASES[example_key]


def build_example_case_data(example_key):
    case = get_example_case(example_key)

    factors = case["factors"]
    factor_cols = [factor["name"] for factor in factors]

    coded_df, real_df, template_df = generate_first_order_design(
        factors=factors,
        center_points=case["center_points"],
        randomize=case["randomize"],
        seed=case["seed"]
    )

    response = simulate_first_order_response(
        coded_df=coded_df,
        factor_cols=factor_cols,
        intercept=case["intercept"],
        coefficients=case["coefficients"],
        noise_sd=case["noise_sd"],
        seed=case["seed"]
    )

    model_df = coded_df[["Corrida"] + factor_cols + ["Tipo"]].copy()
    model_df["Respuesta"] = response
    model_df = model_df[["Corrida"] + factor_cols + ["Respuesta", "Tipo"]]

    real_design_with_response = real_df.copy()
    real_design_with_response[case["response_name"]] = response

    factor_summary = create_factor_summary(factors)

    return {
        "case": case,
        "factor_cols": factor_cols,
        "coded_design": coded_df,
        "real_design": real_df,
        "real_design_with_response": real_design_with_response,
        "template_df": template_df,
        "model_df": model_df,
        "factor_summary": factor_summary,
        "factors": factors,
    }