import json
from pathlib import Path

import pandas as pd

from ..config import get_settings


def get_splits(df: pd.DataFrame):
    """Splits data based on config."""
    cfg = get_settings().splits
    df = df.copy()
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    
    train = df[df["trade_date"] <= pd.to_datetime(cfg.train_end)]
    val = df[(df["trade_date"] > pd.to_datetime(cfg.train_end)) & (df["trade_date"] <= pd.to_datetime(cfg.val_end))]
    holdout = df[df["trade_date"] > pd.to_datetime(cfg.val_end)]
    
    return train, val, holdout

def check_holdout_lock(confirm_holdout: bool = False):
    """Refuses to run on holdout unless confirmed. Logs touches."""
    ledger_path = Path("data/holdout_ledger.json")
    if not confirm_holdout:
        raise PermissionError("Holdout is locked. Pass --confirm-holdout to unlock.")
        
    touches = 0
    if ledger_path.exists():
        with open(ledger_path, "r") as f:
            data = json.load(f)
            touches = data.get("touches", 0)
            
    touches += 1
    with open(ledger_path, "w") as f:
        json.dump({"touches": touches}, f)
        
    return touches
