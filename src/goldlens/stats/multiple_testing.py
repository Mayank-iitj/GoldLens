from statsmodels.stats.multitest import multipletests


def control_fdr(pvalues: list[float], alpha: float = 0.05):
    """Benjamini-Hochberg adjustment."""
    _reject, pvals_corrected, _, _ = multipletests(pvalues, alpha=alpha, method='fdr_bh')
    return pvals_corrected

def bonferroni(pvalues: list[float], alpha: float = 0.05):
    """Bonferroni correction."""
    _reject, pvals_corrected, _, _ = multipletests(pvalues, alpha=alpha, method='bonferroni')
    return pvals_corrected
