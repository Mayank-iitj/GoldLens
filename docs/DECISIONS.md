# Decision Record

This document captures the core quantitative and architectural decisions made for **GoldLens**. Where ambiguity existed, the most defensible option was chosen.

## 1. Statistical Core: Why AR(1) over Augmented Dickey-Fuller (ADF)?
*Context*: We must test whether the residual spread mean-reverts.
*Decision*: While ADF provides a p-value for stationarity, it does not yield a continuous measure of *speed*. We implemented an **Ornstein-Uhlenbeck process calibration via an AR(1) model**.
*Defensibility*: The AR(1) coefficient allows us to extract the half-life of mean reversion ($-\ln(2)/\beta$). If a spread is stationary but its half-life is 120 days, it is fundamentally untradable given the expiry window of the contract. Half-life is actionable; ADF p-values are not.

## 2. Walk-Forward Bias Mitigation: Deflated Sharpe
*Context*: The hackathon requires "honest statistics."
*Decision*: We implemented **Deflated Sharpe Ratio (Bailey & Lopez de Prado, 2014)**.
*Defensibility*: Selecting the best trading parameter (e.g., Z-Score threshold) over many trials inflates the Sharpe ratio due to multiple testing bias (selection bias). Deflated Sharpe probabilistically adjusts the Sharpe ratio downward based on the number of trials and the variance of returns, yielding the true probability that the strategy out-of-sample performance is greater than 0.

## 3. Data Storage: DuckDB over SQLite/Postgres
*Context*: We need to ingest MCX Bhavcopy CSVs efficiently.
*Decision*: We chose **DuckDB**.
*Defensibility*: DuckDB is an in-process SQL OLAP database. It operates on vectorized column-based data, making it orders of magnitude faster than SQLite for time-series quantitative data aggregations.

## 4. UI/UX: Streamlit over React/Next.js
*Context*: The product needs a dashboard.
*Decision*: We chose **Streamlit**.
*Defensibility*: The backend algorithms heavily rely on `pandas`, `statsmodels`, and `scipy`. Forcing this data through REST APIs to a JS frontend adds network overhead and serialisation complexity. Streamlit allows native Python dataframes to be passed directly to the presentation layer via `plotly`, minimising latency and architectural bloat.

## 5. The Verdict: "NO-GO"
*Context*: Does a profitable carry-adjusted spread exist?
*Decision*: The pipeline yields a definitive NO-GO.
*Defensibility*: "No persistent edge survives costs." While naive z-score spreads appear profitable, adjusting for the time-value-of-money carry (due to the 3rd-5th vs 27th-31st maturity mismatch) flattens the edge. Subjecting the residual edge to CTT (Commodities Transaction Tax) and slippage removes the rest. An honest system declares a NO-GO rather than overfitting to force profitability.
