import numpy as np


def block_bootstrap(series, block_size=10, n_bootstraps=1000):
    """Block bootstrap for time series to estimate confidence intervals."""
    if len(series) < block_size * 2:
        return np.nan, np.nan
        
    n = len(series)
    num_blocks = n // block_size
    blocks = [series.iloc[i*block_size : (i+1)*block_size] for i in range(num_blocks)]
    
    means = []
    for _ in range(n_bootstraps):
        sample_blocks = [blocks[i] for i in np.random.randint(0, num_blocks, num_blocks)]
        sample = np.concatenate(sample_blocks)
        means.append(np.mean(sample))
        
    return np.percentile(means, 2.5), np.percentile(means, 97.5)
