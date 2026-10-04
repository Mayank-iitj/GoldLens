import duckdb

from ..config import get_settings


class SuppressionLog:
    def __init__(self):
        self.conn = duckdb.connect(get_settings().database_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS suppression_log (
                trade_date DATE,
                pair VARCHAR,
                reason VARCHAR
            )
        """)
        
    def log(self, trade_date, pair, reasons):
        if not reasons:
            return
        
        reasons_str = "; ".join(reasons)
        self.conn.execute("""
            INSERT INTO suppression_log (trade_date, pair, reason) 
            VALUES (?, ?, ?)
        """, (trade_date, pair, reasons_str))
