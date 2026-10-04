from .gates import run_gates
from .suppression_log import SuppressionLog
import logging

log = logging.getLogger(__name__)

def evaluate_alerts(date, pair, z, expected_reversion, est_costs, stationary, half_life):
    """Runs gates and logs suppressions or fires alerts."""
    passed, reasons = run_gates(z, expected_reversion, est_costs, stationary, half_life)
    
    if passed:
        log.info(f"ALERT FIRED: {pair} on {date}. Edge: {expected_reversion - est_costs}")
        return True
    else:
        logger = SuppressionLog()
        logger.log(date, pair, reasons)
        return False
