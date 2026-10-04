import pandas as pd
import numpy as np
import statsmodels.api as sm
import logging

log = logging.getLogger(__name__)

def fit_implied_carry(group: pd.DataFrame):
    """Regress log(norm_close) on tte_years to find continuous annualized carry."""
    if len(group) < 2:
        return pd.Series({"carry_rate": 0.0, "intercept": np.nan, "fitted": False})
        
    y = np.log(group["norm_close"].astype(float))
    X = sm.add_constant(group["tte_years"].astype(float))
    
    try:
        model = sm.RLM(y, X, M=sm.robust.norms.HuberT())
        results = model.fit()
        carry_rate = results.params.get("tte_years", 0.0)
        intercept = results.params.get("const", y.mean())
        return pd.Series({"carry_rate": carry_rate, "intercept": intercept, "fitted": True})
    except Exception as e:
        log.debug(f"Robust fit failed: {e}")
        return pd.Series({"carry_rate": 0.0, "intercept": np.nan, "fitted": False})

def build_implied_carry(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    carry = df.groupby(["trade_date", "symbol"]).apply(fit_implied_carry).reset_index()
    return carry
