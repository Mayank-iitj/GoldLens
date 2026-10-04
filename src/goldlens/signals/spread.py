import itertools

import pandas as pd


def compute_spreads(df: pd.DataFrame, target_symbols: list[str]) -> pd.DataFrame:
    """Compute naive and carry-adjusted spread for all pairs."""
    if df.empty:
        return pd.DataFrame()
        
    pairs = list(itertools.combinations(target_symbols, 2))
    spreads = []
    
    pivot_naive = df.pivot(index="trade_date", columns="symbol", values="norm_close")
    pivot_adj = df.pivot(index="trade_date", columns="symbol", values="carry_adj_norm_close")
    
    for s1, s2 in pairs:
        if s1 in pivot_naive.columns and s2 in pivot_naive.columns:
            naive = pivot_naive[s1] - pivot_naive[s2]
            adj = pivot_adj[s1] - pivot_adj[s2]
            
            temp = pd.DataFrame({
                "trade_date": naive.index,
                "pair": f"{s1}_{s2}",
                "leg1": s1,
                "leg2": s2,
                "naive_spread": naive,
                "adj_spread": adj
            }).dropna()
            spreads.append(temp)
            
    return pd.concat(spreads, ignore_index=True) if spreads else pd.DataFrame()
