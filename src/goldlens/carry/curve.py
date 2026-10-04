import pandas as pd

def build_term_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Computes days to expiry."""
    if df.empty:
        return df
    df = df.copy()
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df["expiry_date"] = pd.to_datetime(df["expiry_date"])
    df["dte"] = (df["expiry_date"] - df["trade_date"]).dt.days
    df["tte_years"] = df["dte"] / 365.0
    return df
