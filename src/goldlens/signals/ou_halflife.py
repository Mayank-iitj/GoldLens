import numpy as np
import pandas as pd
import statsmodels.api as sm


def compute_ou_halflife(series: pd.Series) -> float:
    """Computes Ornstein-Uhlenbeck half-life via AR(1)."""
    series = series.dropna()
    if len(series) < 10:
        return np.nan
        
    y = series.diff().dropna()
    X = sm.add_constant(series.shift(1).dropna())
    
    y, X = y.align(X, join='inner')
    
    try:
        model = sm.OLS(y, X).fit()
        b = model.params.iloc[1]
        
        if b >= 0:
            return np.nan
            
        return float(-np.log(2) / b)
    except Exception:  # noqa: BLE001
        return np.nan
