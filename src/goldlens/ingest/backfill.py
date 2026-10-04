import logging
import time
from datetime import date, timedelta
from io import BytesIO
from pathlib import Path

import pandas as pd

from ..config import get_settings
from .mcx_client import MCXClient
from .parser import parse_bhavcopy
from .store import Store
from .validator import validate_bhavcopy_date

log = logging.getLogger(__name__)

def run_backfill(start_str: str, end_str: str):
    start_date = pd.to_datetime(start_str).date()
    end_date = date.today()  # noqa: DTZ011 if end_str == "today" else pd.to_datetime(end_str).date()
    
    settings = get_settings()
    allowed_symbols = list(settings.contracts.keys())
    
    client = MCXClient()
    store = Store()
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    curr = start_date
    while curr <= end_date:
        if curr.weekday() >= 5: # Skip weekends
            curr += timedelta(days=1)
            continue
            
        raw_path = raw_dir / f"{curr.strftime('%Y%m%d')}.csv"
        
        try:
            if raw_path.exists():
                with open(raw_path, "rb") as f:
                    raw_csv = f.read()
            else:
                raw_csv = client.fetch_bhavcopy(curr)
                with open(raw_path, "wb") as f:
                    f.write(raw_csv)
                time.sleep(1) # Polite scraping
            
            df = parse_bhavcopy(BytesIO(raw_csv), allowed_symbols)
            if not df.empty:
                df = validate_bhavcopy_date(df, curr)
                
            if not df.empty:
                store.upsert_bhavcopy(df)
                store.log_quality(curr, "OK", "Success", curr)
            else:
                store.log_quality(curr, "DISCARD", "Failed validation or empty", None)
                
        except Exception as e:  # noqa: BLE001
            log.error(f"Error on {curr}: {e}")
            store.log_quality(curr, "ERROR", str(e), None)
            
        curr += timedelta(days=1)
