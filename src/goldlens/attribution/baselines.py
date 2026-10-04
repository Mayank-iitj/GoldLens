import pandas as pd

def naive_buy_and_hold(gold_series: pd.Series) -> pd.Series:
    """Returns buy and hold PnL stream."""
    return gold_series.diff()

def placebo_spread(spread_series: pd.Series) -> pd.Series:
    """Shuffles spread changes to destroy serial correlation (no edge placebo)."""
    changes = spread_series.diff().dropna()
    shuffled = changes.sample(frac=1).reset_index(drop=True)
    return shuffled
