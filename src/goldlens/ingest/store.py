import duckdb
import pandas as pd
from pathlib import Path
from ..config import get_settings

class Store:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or get_settings().database_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(self.db_path)
        self._init_tables()
        
    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS bhavcopy (
                trade_date DATE,
                symbol VARCHAR,
                expiry_date DATE,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume DOUBLE,
                open_interest DOUBLE,
                PRIMARY KEY (symbol, expiry_date, trade_date)
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS data_quality (
                requested_date DATE PRIMARY KEY,
                status VARCHAR,
                reason VARCHAR,
                actual_date DATE
            )
        """)
        
    def upsert_bhavcopy(self, df: pd.DataFrame):
        if df.empty:
            return
        
        records = df[["Date", "Symbol", "ExpiryDate", "Open", "High", "Low", "Close", "Volume", "OpenInterest"]].copy()
        records["Date"] = pd.to_datetime(records["Date"]).dt.date
        records["ExpiryDate"] = pd.to_datetime(records["ExpiryDate"]).dt.date
        
        # Deduplicate
        records = records.drop_duplicates(subset=["Symbol", "ExpiryDate", "Date"])
        
        self.conn.execute("""
            INSERT INTO bhavcopy 
            SELECT * FROM records
            ON CONFLICT (symbol, expiry_date, trade_date) DO UPDATE SET
                open = excluded.open,
                high = excluded.high,
                low = excluded.low,
                close = excluded.close,
                volume = excluded.volume,
                open_interest = excluded.open_interest
        """)
        
    def log_quality(self, requested_date, status, reason, actual_date=None):
        self.conn.execute("""
            INSERT INTO data_quality (requested_date, status, reason, actual_date)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (requested_date) DO UPDATE SET
                status = excluded.status,
                reason = excluded.reason,
                actual_date = excluded.actual_date
        """, (requested_date, status, reason, actual_date))
