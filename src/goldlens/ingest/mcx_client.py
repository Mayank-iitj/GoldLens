import logging
from datetime import date

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

log = logging.getLogger(__name__)

class MCXClient:
    def __init__(self):
        self.base_url = "https://www.mcxindia.com/market-data/bhavcopy"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*"
        }

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
    def fetch_bhavcopy(self, target_date: date) -> bytes:
        # MCX Bhavcopy endpoint typically uses ASPX postbacks or specific routes.
        # This mocks the network layer structure with retries as requested.
        # We assume returning CSV bytes.
        url = "https://www.mcxindia.com/backpage.aspx/GetDateWiseBhavCopy"
        payload = {"Date": target_date.strftime("%d/%m/%Y")}
        try:
            with httpx.Client() as client:
                r = client.post(url, json=payload, headers=self.headers, timeout=10.0)
                r.raise_for_status()
                # For this exercise, if the payload is json containing HTML/CSV, we extract it.
                # In practice, we just return the bytes.
                return r.content
        except Exception as e:
            log.warning(f"Failed fetching {target_date}: {e}")
            raise
