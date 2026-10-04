import numpy as np
import pandas as pd


def calculate_metrics(pnl_series: pd.Series, risk_free_rate: float = 0.0) -> dict:
    """Standard backtest metrics."""
    if pnl_series.empty:
        return {}
        
    pnl = pnl_series.dropna()
    cum_pnl = pnl.cumsum()
    
    total_ret = cum_pnl.iloc[-1] if len(cum_pnl) > 0 else 0.0
    
    mean_pnl = pnl.mean()
    std_pnl = pnl.std()
    
    sharpe = (mean_pnl / std_pnl * np.sqrt(252)) if std_pnl > 0 else 0.0
    
    roll_max = cum_pnl.cummax()
    drawdown = cum_pnl - roll_max
    max_dd = drawdown.min()
    
    down_pnl = pnl[pnl < 0]
    down_std = down_pnl.std()
    sortino = (mean_pnl / down_std * np.sqrt(252)) if down_std > 0 else 0.0
    
    return {
        "Total PnL": total_ret,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max Drawdown": max_dd,
        "Hit Rate": (pnl > 0).mean(),
        "Win Rate": (pnl[pnl > 0].sum() / -pnl[pnl < 0].sum()) if len(pnl[pnl < 0]) > 0 else np.nan
    }
