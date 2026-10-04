<div align="center">

# 🏦 GoldLens
**Commodity Derivatives Intelligence & Carry-Adjusted Relative Value Analytics**

[![Hackathon](https://img.shields.io/badge/Hack_in_Hills_'26-PS_03-f2a900?style=for-the-badge&logo=hackaday&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-Production-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](#)

*An ultra-premium, production-grade statistical pipeline for analyzing MCX Gold futures. Built on the philosophy that true edge must survive structural friction.*

</div>

---

## 🛑 The Verdict: Why We Say "NO-GO"
In quantitative finance, presenting a profitable naive strategy is easy. **Protecting capital is hard.** 

Most platforms look at the price difference between `GOLDM` and `GOLDTEN` and see a profitable arbitrage. **GoldLens tells the truth.** By rigorously stripping out the time-value-of-money (the maturity mismatch) and subjecting the residual edge to MCX Commodities Transaction Taxes (CTT) and slippage, GoldLens proves the structural mispricing does *not* survive trading frictions. We proudly present a **NO-GO** verdict, demonstrating institutional honesty over synthetic overfitting.

---

## 🎯 Problem Statement (Hack in Hills '26 - PS 03)
**Objective:** Turn MCX daily Bhavcopy settlement data into a defensible analytical product.

GoldLens systematically solves all four parameters of the prompt:
1. **Unit Normalization:** Converts 100g, 8g, and 1g contracts (995 & 999 purity) to a standardized baseline.
2. **Carry-Adjustment:** Extracts the time-to-expiry decay caused by the `GOLDM` (3rd-5th) vs `GOLDTEN` (27th-31st) maturity mismatch.
3. **Mean-Reversion Proof:** Proves stationarity using Ornstein-Uhlenbeck AR(1) modeling rather than basic Dickey-Fuller p-values.
4. **Walk-Forward Backtesting:** Strictly quarantined out-of-sample testing with Deflated Sharpe metrics to penalize multiple-testing bias.

---

## 🧠 Core Architecture

GoldLens is divided into two breathtaking user experiences backed by a heavy-duty Python engine.

- **The Explorer (`planet_jumping.html`):** A cinematic, 3D WebGL-powered portal built in a single self-contained file. It serves as an immersive marketing landing page introducing the MCX Gold universe.
- **The Terminal (`app/streamlit_app.py`):** A dark-themed, ultra-premium quantitative dashboard processing Pandas DataFrames and `statsmodels` math in real-time.
- **The Engine (`src.goldlens`):** A highly modularized backend pipeline architected around DuckDB for vectorized ingestion and SciPy for probability distributions.

---

## 📊 Terminal Features

| Feature | Description |
|---------|-------------|
| **Normalization Engine** | Real-time visual tracking of price convergence after adjusting for lot sizes and purity scalars. |
| **Term Structure Extraction** | Isolates the "Implied Carry" yield curve, separating pure alpha from standard financing costs. |
| **OU Half-Life Calibration** | Scatter plots of daily spread changes against lagged levels, proving mean-reversion speed via $\beta$. |
| **Equity Trajectory** | Directly contrasts Gross PnL (the illusion) against Net PnL (the post-CTT reality). |

---

## 🚀 Quickstart

Run the pipeline and launch the terminal locally in seconds.

```bash
# 1. Install dependencies via Poetry (or standard pip)
poetry install

# 2. Ingest the Data (Optional if running in Simulation Mode)
poetry run python -m goldlens.cli ingest --start 2023-01-01 --end today

# 3. Launch the Quantitative Terminal
poetry run streamlit run app/streamlit_app.py
```

*Alternatively, open `planet_jumping.html` in your browser for the cinematic preamble, then click **Launch Terminal**.*

---

## 📚 Documentation
- **[Decisions Log](docs/DECISIONS.md):** The math and logic behind our strictly lagged Z-scores and Deflated Sharpe thresholds.
- **[Architecture](docs/ARCHITECTURE.md):** Detailed breakdown of the DuckDB data lake.
- **[Pitch Script](docs/DEMO_SCRIPT.md):** The 3-minute hackathon presentation track.

<div align="center">
  <br>
  <i>"No persistent edge survives costs." — The GoldLens Philosophy</i>
</div>
