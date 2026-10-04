from ..config import get_settings

def generate_verdict(pair: str, stats: dict) -> dict:
    """Decision rule for GO/NO-GO."""
    cfg = get_settings().verdict
    reasons = []
    
    if stats.get("deflated_sharpe", 0) < cfg.min_deflated_sharpe:
        reasons.append(f"Deflated Sharpe {stats.get('deflated_sharpe')} < {cfg.min_deflated_sharpe}")
        
    if abs(stats.get("beta", 1)) > cfg.max_beta:
        reasons.append(f"Beta {stats.get('beta')} > {cfg.max_beta}")
        
    if not stats.get("stationary", False):
        reasons.append("Spread is not stationary")
        
    if stats.get("net_edge_bps", -1) <= 0:
        reasons.append("Net edge after costs is negative")
        
    status = "GO" if not reasons else "NO-GO"
    
    return {
        "pair": pair,
        "status": status,
        "reasons": reasons,
        "stats": stats
    }
