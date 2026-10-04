# Threats of Bias

1. **Look-ahead Bias**: Signal generated on close T is executed at close T+1. We must execute at next day's price or apply a slippage penalty.
2. **Survivorship Bias**: All contracts are included if they existed.
3. **Data Snooping**: Z-score window, entry/exit thresholds are prone to overfitting. We use a locked holdout set and Deflated Sharpe Ratio to adjust for the number of trials.
