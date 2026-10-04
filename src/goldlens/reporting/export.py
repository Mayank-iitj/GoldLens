import pandas as pd
import json

def export_verdict_json(verdict_data: dict, filepath: str):
    """Exports verdict dictionary to JSON."""
    with open(filepath, 'w') as f:
        json.dump(verdict_data, f, indent=4)
        
def export_results_csv(df: pd.DataFrame, filepath: str):
    """Exports backtest results to CSV."""
    df.to_csv(filepath, index=False)
