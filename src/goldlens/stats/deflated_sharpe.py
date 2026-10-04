import numpy as np
from scipy.stats import norm

def deflated_sharpe_ratio(observed_sharpe: float, trials: int, T: int) -> float:
    """Computes Deflated Sharpe Ratio (Bailey & Lopez de Prado 2014) probability."""
    if trials < 1:
        trials = 1
    # Expected maximum Sharpe of independent trials (approximation)
    emax = np.sqrt(2 * np.log(trials)) if trials > 1 else 0.0
    # True DSR requires variance of Sharpe across trials, we use simplified E[Max(SR)]
    psr = norm.cdf((observed_sharpe - emax) * np.sqrt(T - 1))
    return float(psr)
