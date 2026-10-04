from ..config import get_costs


def estimate_slippage(high: float, low: float, vol_percentile: float) -> float:
    """Estimates slippage based on high-low range and liquidity."""
    cfg = get_costs().slippage
    slip = cfg.k * (high - low)
    if vol_percentile < 0.25:
        slip *= cfg.thin_multiplier
    return slip
