# Methodology

## 1. Normalization
Contracts are normalized to INR per 1 gram at 999 purity.
GOLDM (995 purity): `Price / 10 * (999/995)`

## 2. Carry Adjustment
Naive spreads suffer from maturity mismatch (e.g. 5th vs 30th expiry). We fit a term structure using live expiries per trade date:
`log(Price) ~ time_to_expiry`
We interpolate prices to a common target maturity (e.g. 30 days) to strip out mechanical roll-down.

## 3. Signal Generation
Residual = Adjusted Spread - Structural Premium (estimated on train set).
Rolling Z-score of the residual dictates entry and exit.

## 4. Cost Model
Costs strictly reflect MCX rates (CTT, Exchange txn, GST) plus broker commissions on the notional size of the exact lots held.
