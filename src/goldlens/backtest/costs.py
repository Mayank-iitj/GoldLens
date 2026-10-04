import logging

from ..config import get_costs

log = logging.getLogger(__name__)

def compute_trade_costs(price: float, lot_size: int, action: str) -> float:
    """Computes full trading costs for one leg based on MCX schedule."""
    cfg = get_costs()
    notional = price * lot_size
    
    # Brokerage
    brokerage = cfg.brokerage.rate if cfg.brokerage.type == "flat" else (cfg.brokerage.rate * notional)
    
    # Exchange
    exch_txn = cfg.exchange_txn_charge.rate * notional
    
    # CTT (only on sell side)
    ctt = cfg.ctt.rate * notional if action.upper() == "SELL" else 0.0
    
    # GST
    gst = cfg.gst.rate * (brokerage + exch_txn)
    
    # SEBI
    sebi = cfg.sebi_fee.rate * notional
    
    # Stamp Duty (only on buy side)
    stamp = cfg.stamp_duty.rate * notional if action.upper() == "BUY" else 0.0
    
    return brokerage + exch_txn + ctt + gst + sebi + stamp
