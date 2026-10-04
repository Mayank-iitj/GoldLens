import pandas as pd
import statsmodels.api as sm

def compute_attribution(strategy_pnl: pd.Series, gold_returns: pd.Series):
    """OLS regression to separate alpha and beta."""
    strategy_pnl = strategy_pnl.dropna()
    gold_returns = gold_returns.dropna()
    
    aligned = pd.concat([strategy_pnl, gold_returns], axis=1).dropna()
    if len(aligned) < 10:
        return {"alpha": 0.0, "beta": 0.0, "r2": 0.0, "alpha_tstat": 0.0, "beta_tstat": 0.0}
        
    y = aligned.iloc[:, 0]
    X = sm.add_constant(aligned.iloc[:, 1])
    
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 1})
    
    return {
        "alpha": model.params.iloc[0] * 252, # annualized intercept
        "beta": model.params.iloc[1],
        "r2": model.rsquared,
        "alpha_tstat": model.tvalues.iloc[0],
        "beta_tstat": model.tvalues.iloc[1]
    }
