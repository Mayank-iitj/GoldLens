import pandas as pd


def parse_bhavcopy(raw_csv_bytes, allowed_symbols: list[str]) -> pd.DataFrame:
    try:
        df = pd.read_csv(raw_csv_bytes)
    except Exception:  # noqa: BLE001
        return pd.DataFrame()
        
    df.columns = [c.strip() for c in df.columns]
    
    if "InstrumentName" in df.columns:
        df = df[df["InstrumentName"] == "FUTCOM"]
        
    if "Symbol" not in df.columns:
        return pd.DataFrame()
        
    df["Symbol"] = df["Symbol"].astype(str).str.strip()
    df = df[df["Symbol"].isin(allowed_symbols)]
    
    if df.empty:
        return df
        
    # ExpiryDate
    df["ExpiryDate"] = pd.to_datetime(df["ExpiryDate"], format="%d%b%Y", errors='coerce')
    
    # Numeric columns
    num_cols = ["Open", "High", "Low", "Close", "Volume", "OpenInterest"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Reject bad prices
    bad_idx = (df["High"] < df["Low"]) | (df["Close"] < df["Low"]) | (df["Close"] > df["High"]) | (df["Close"] < 0)
    df = df[~bad_idx]
    
    return df
