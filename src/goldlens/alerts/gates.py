from ..config import get_settings


def run_gates(z: float, expected_reversion: float, est_costs: float, stationary: bool, half_life: float):
    """Evaluates if an alert should fire."""
    cfg = get_settings().signal
    reasons = []
    
    if abs(z) < cfg.z_entry:
        reasons.append("Z-score below entry")
        
    if not stationary:
        reasons.append("Spread not stationary")
        
    if expected_reversion < est_costs * 1.5:
        reasons.append("Edge < 1.5x Costs")
        
    if half_life > cfg.half_life_max:
        reasons.append(f"Half life {half_life} > {cfg.half_life_max}")
        
    return len(reasons) == 0, reasons
