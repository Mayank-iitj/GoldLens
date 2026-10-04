import logging
from datetime import timedelta

import pandas as pd

log = logging.getLogger(__name__)

def build_lifecycle(df: pd.DataFrame, volume_pct: float = 0.5) -> pd.DataFrame:
    """Builds contract lifecycle dates (listing, liquidity_ready, tender, expiry)."""
    if df.empty:
        return pd.DataFrame()
        
    lifecycle = []
    
    for (symbol, expiry), group in df.groupby(["symbol", "expiry_date"]):
        group = group.sort_values("trade_date")
        listing_date = group["trade_date"].iloc[0]
        expiry_date = group["trade_date"].iloc[-1]
        
        vol_thresh = df["volume"].quantile(volume_pct)
        liq_days = group[group["volume"] > vol_thresh]
        liq_ready = liq_days["trade_date"].iloc[0] if not liq_days.empty else listing_date
        
        tender_start = expiry_date - timedelta(days=5)
        
        lifecycle.append({
            "symbol": symbol,
            "expiry_date": expiry,
            "listing_date": listing_date,
            "liquidity_ready": liq_ready,
            "tender_start": tender_start,
            "last_trade_date": expiry_date
        })
        
    return pd.DataFrame(lifecycle)
