import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

def test_stationarity(series: pd.Series):
    """ADF and KPSS tests for stationarity."""
    series = series.dropna()
    if len(series) < 20:
        return {"adf_stat": None, "adf_pvalue": None, "kpss_stat": None, "kpss_pvalue": None, "stationary": False}
        
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            adf = adfuller(series, autolag='AIC')
            kpss_test = kpss(series, regression='c', nlags="auto")
            
        adf_p = adf[1]
        kpss_p = kpss_test[1]
        
        stationary = (adf_p < 0.05) and (kpss_p > 0.05)
        
        return {
            "adf_stat": adf[0],
            "adf_pvalue": adf_p,
            "kpss_stat": kpss_test[0],
            "kpss_pvalue": kpss_p,
            "stationary": stationary
        }
    except:
        return {"adf_stat": None, "adf_pvalue": None, "kpss_stat": None, "kpss_pvalue": None, "stationary": False}
