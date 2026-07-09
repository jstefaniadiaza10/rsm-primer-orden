import pandas as pd


def fit_first_order_model(
    model_df,
    factor_cols,
    response_col="Respuesta",
    response_label="Respuesta"
):
    """
    Ajusta un modelo lineal de primer orden:

        Y = beta0 + beta1*X1 + beta2*X2 + ... + error

    La importación de statsmodels se hace dentro de la función para evitar
    que la página cargue lenta al abrirse.
    """

    import statsmodels.api as sm

    if response_col not in model_df.columns:
        raise ValueError(f"No existe la columna de respuesta: {response_col}")

    if not factor_cols:
        raise ValueError("No se identificaron factores para el modelo.")

    data = model_df.copy()

    for col in factor_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data[response_col] = pd.to_numeric(data[response_col], errors="coerce")

    if data[factor_cols + [response_col]].isna().sum().sum() > 0:
        raise ValueError("Existen valores faltantes o no numéricos en la base.")

    X = data[factor_cols]
    y = data[response_col]

    X_const = sm.add_constant(X)

    model = sm.OLS(y, X_const).fit()

    fitted = model.fittedvalues
    residuals = model.resid

    results_df = data.copy()
    results_df["Ajustado"] = fitted
    results_df["Residuo"] = residuals

    coef_df = pd.DataFrame({
        "Parámetro": model.params.index,
        "Coeficiente": model.params.values,
        "Error estándar": model.bse.values,
        "t": model.tvalues.values,
        "p-valor": model.pvalues.values
    })

    equation = build_equation(
        params=model.params,
        response_label=response_label
    )

    return {
        "model": model,
        "coef_df": coef_df,
        "results_df": results_df,
        "r2": model.rsquared,
        "r2_adj": model.rsquared_adj,
        "aic": model.aic,
        "bic": model.bic,
        "equation": equation
    }


def build_equation(params, response_label="Respuesta"):
    """
    Construye una ecuación legible del modelo estimado.
    """

    terms = []

    for name, value in params.items():
        if name == "const":
            terms.append(f"{value:.4f}")
        else:
            sign = "+" if value >= 0 else "-"
            terms.append(f"{sign} {abs(value):.4f}·{name}")

    return f"{response_label} estimado = " + " ".join(terms)