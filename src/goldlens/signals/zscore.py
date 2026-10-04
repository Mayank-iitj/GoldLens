import pandas as pd

from ..config import get_settings


def rolling_zscore(spread_series: pd.Series, window: int | None = None) -> pd.Series:
    """Rolling zscore strictly lagged."""
    if window is None:
        window = get_settings().signal.z_window
        
    roll_mean = spread_series.shift(1).rolling(window).mean()
    roll_std = spread_series.shift(1).rolling(window).std()
    
    return (spread_series - roll_mean) / roll_std
