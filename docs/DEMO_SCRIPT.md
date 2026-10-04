# GoldLens - Demo Script (3 Minutes)

This script is designed for the Hackathon presentation to showcase the robustness and honesty of the GoldLens system.

### Step 1: The Cinematic Introduction (0:00 - 0:45)
- **Action:** Open `planet_jumping.html` in the browser.
- **Talking Track:** "Welcome to GoldLens. To understand the problem, you have to understand the universe of MCX Gold contracts. GOLDM is the institutional benchmark expiring early in the month. GOLDTEN and GOLDGUINEA expire at the end of the month. This maturity mismatch creates artificial spreads. We built GoldLens to cut through the noise."
- **Action:** Click **Launch Terminal**.

### Step 2: The Honest Verdict (0:45 - 1:30)
- **Action:** Show the "Overview & Verdict" tab in Streamlit.
- **Talking Track:** "Most systems will show you a profitable spread and stop there. GoldLens tells you the truth: it's a NO-GO. Why? Because while the raw spread looks highly mean-reverting (half-life of 6 days), once we adjust for the carry/maturity mismatch, the edge shrinks. When we add CTT and slippage, the edge vanishes. Deflated Sharpe confirms the probability of success is a failure."

### Step 3: Real Quant Architecture (1:30 - 2:30)
- **Action:** Click the "Walk-Forward Backtest" and "Methodology" tabs.
- **Talking Track:** "Under the hood, we are using production-grade algorithms. We use DuckDB for columnar speed, Ornstein-Uhlenbeck AR(1) models for half-life extraction, and strictly lagged Z-scores. We quarantined a 30% holdout set to ensure no lookahead bias."

### Step 4: Conclusion (2:30 - 3:00)
- **Talking Track:** "GoldLens is Commodity Derivatives Intelligence. It’s not just a UI; it’s a defensible, mathematically honest pipeline that protects capital by preventing false-positive trades. Thank you."
