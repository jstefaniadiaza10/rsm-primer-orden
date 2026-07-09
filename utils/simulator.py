import numpy as np
import pandas as pd


def simulate_first_order_response(
    coded_df: pd.DataFrame,
    factor_cols: list,
    intercept: float = 80.0,
    coefficients: dict | None = None,
    noise_sd: float = 1.0,
    seed: int = 123,
    decimals: int = 2
) -> pd.Series:
    """
    Simula una respuesta experimental para un diseño de primer orden.

    Modelo usado:
        Y = beta0 + beta1*X1 + beta2*X2 + ... + error

    Las variables X deben estar codificadas en -1, 0, 1.
    """

    if coefficients is None:
        coefficients = {factor: 1.0 for factor in factor_cols}

    rng = np.random.default_rng(seed)

    X = coded_df[factor_cols].astype(float)

    beta = np.array([
        coefficients.get(factor, 0.0)
        for factor in factor_cols
    ])

    y = intercept + X.values @ beta

    if noise_sd > 0:
        y = y + rng.normal(
            loc=0,
            scale=noise_sd,
            size=len(coded_df)
        )

    return pd.Series(
        np.round(y, decimals),
        index=coded_df.index
    )