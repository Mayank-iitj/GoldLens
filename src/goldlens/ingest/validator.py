from datetime import date
import pandas as pd
import logging

log = logging.getLogger(__name__)

def validate_bhavcopy_date(df: pd.DataFrame, requested_date: date) -> pd.DataFrame:
    if df.empty:
        log.warning(f"Discarding: Empty payload for {requested_date}")
        return pd.DataFrame()
    
    if "Date" not in df.columns:
        log.warning(f"Discarding: No Date column for {requested_date}")
        return pd.DataFrame()

    # Determine actual date from payload
    parsed_dates = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors='coerce')
    if parsed_dates.isnull().all():
        parsed_dates = pd.to_datetime(df["Date"], errors='coerce')
        
    actual_date = parsed_dates.mode()[0].date() if not parsed_dates.empty else None

    if actual_date != requested_date:
        log.warning(f"Discarding {requested_date}: returned data for {actual_date}")
        return pd.DataFrame()
    
    return df
