# Architecture

GoldLens is designed as a monolithic pipeline focused on speed, numerical accuracy, and ease of deployment.

## Tech Stack
- **Language**: Python 3.11+
- **Database**: DuckDB (OLAP, columnar)
- **Quant Libraries**: `pandas`, `numpy`, `statsmodels`, `scipy`
- **Dashboard**: `streamlit`, `plotly`
- **Dependency Management**: `poetry`

## Pipeline Overview

1. **Ingestion (`src.goldlens.ingest`)**
   - Retrieves MCX Bhavcopy data.
   - Cleans and normalizes units (e.g. GOLDM -> 10g, GOLDGUINEA -> 8g).
   - Upserts into `data/goldlens.duckdb`.

2. **Carry Adjustment (`src.goldlens.carry`)**
   - Calculates time to expiry.
   - Fits a robust log-linear term structure.
   - Strips maturity mismatch out of the spread.

3. **Signals & Statistics (`src.goldlens.signals`, `src.goldlens.stats`)**
   - Calculates Ornstein-Uhlenbeck half-life.
   - Generates strictly lagged Z-scores to prevent look-ahead bias.
   - Applies Bailey & Lopez de Prado's Deflated Sharpe.

4. **Presentation (`app.streamlit_app`)**
   - Serves the final analytics and verdicts to the end user.
