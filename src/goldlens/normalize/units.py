import pandas as pd

from ..config import get_settings


def normalize_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize prices to INR per gram, 999 purity."""
    if df.empty:
        return df
        
    df = df.copy()
    settings = get_settings()
    
    def get_multiplier(symbol):
        spec = settings.contracts.get(symbol)
        if not spec:
            return 1.0
        return (1.0 / spec.base_unit) * (999.0 / spec.purity)
        
    df["norm_multiplier"] = df["symbol"].map(get_multiplier)
    
    for col in ["open", "high", "low", "close"]:
        if col in df.columns:
            df[f"norm_{col}"] = df[col] * df["norm_multiplier"]
            
    return df
