import pandas as pd
import numpy as np

def apply_carry_adjustment(df: pd.DataFrame, carry_df: pd.DataFrame, target_dte: int = 30) -> pd.DataFrame:
    """Adjust normalized prices to a common target DTE."""
    if df.empty or carry_df.empty:
        return df
        
    df = df.merge(carry_df, on=["trade_date", "symbol"], how="left")
    df["carry_rate"] = df["carry_rate"].fillna(0.0)
    
    target_tte = target_dte / 365.0
    carry_factor = np.exp(df["carry_rate"] * (target_tte - df["tte_years"]))
    df["carry_adj_norm_close"] = df["norm_close"] * carry_factor
    
    return df
