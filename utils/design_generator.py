import itertools
import pandas as pd
import numpy as np


def generate_first_order_design(factors, center_points=0, randomize=False, seed=123):
    """
    Genera un diseño factorial completo 2^k con puntos centrales.

    Parameters
    ----------
    factors : list of dict
        Lista con diccionarios:
        [
            {"name": "Temperatura", "low": 160, "high": 180},
            {"name": "Tiempo", "low": 10, "high": 20}
        ]

    center_points : int
        Número de puntos centrales.

    randomize : bool
        Si True, aleatoriza el orden de corridas.

    seed : int
        Semilla para reproducibilidad.

    Returns
    -------
    coded_df : pandas.DataFrame
        Matriz codificada en niveles -1, 0, 1.

    real_df : pandas.DataFrame
        Matriz en unidades reales.

    template_df : pandas.DataFrame
        Plantilla para que el usuario ingrese la respuesta experimental.
    """

    if not factors:
        raise ValueError("Debe ingresar al menos un factor.")

    factor_names = [f["name"] for f in factors]

    # Validaciones
    for f in factors:
        if f["name"].strip() == "":
            raise ValueError("Todos los factores deben tener nombre.")

        if f["low"] >= f["high"]:
            raise ValueError(
                f"El nivel bajo debe ser menor que el nivel alto en el factor: {f['name']}"
            )

    # Diseño factorial 2^k
    coded_levels = list(itertools.product([-1, 1], repeat=len(factors)))
    coded_df = pd.DataFrame(coded_levels, columns=factor_names)

    # Puntos centrales
    if center_points > 0:
        center_df = pd.DataFrame(
            np.zeros((center_points, len(factors))),
            columns=factor_names
        )
        coded_df = pd.concat([coded_df, center_df], ignore_index=True)

    # Aleatorización
    if randomize:
        coded_df = coded_df.sample(frac=1, random_state=seed).reset_index(drop=True)

    coded_df.insert(0, "Corrida", range(1, len(coded_df) + 1))

    # Transformación a unidades reales
    real_df = coded_df.copy()

    for f in factors:
        name = f["name"]
        low = f["low"]
        high = f["high"]

        center = (high + low) / 2
        step = (high - low) / 2

        real_df[name] = center + coded_df[name] * step

    # Identificar puntos centrales
    coded_df["Tipo"] = np.where(
        coded_df[factor_names].abs().sum(axis=1) == 0,
        "Centro",
        "Factorial"
    )

    real_df["Tipo"] = coded_df["Tipo"]

    # Plantilla para registrar respuesta
    template_df = real_df.copy()
    template_df["Respuesta"] = ""

    return coded_df, real_df, template_df


def create_factor_summary(factors):
    """
    Crea una tabla resumen de factores, niveles y punto central.
    """

    rows = []

    for f in factors:
        low = f["low"]
        high = f["high"]
        center = (low + high) / 2
        step = (high - low) / 2

        rows.append({
            "Factor": f["name"],
            "Nivel bajo (-1)": low,
            "Centro (0)": center,
            "Nivel alto (+1)": high,
            "Semirango": step
        })

    return pd.DataFrame(rows)