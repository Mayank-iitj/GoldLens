import numpy as np
import pandas as pd

from ..config import get_settings
from ..contracts.specs import get_contract_spec


class BacktestEngine:
    def __init__(self, data: pd.DataFrame, lifecycle: pd.DataFrame):
        self.data = data
        self.lifecycle = lifecycle
        self.settings = get_settings()
        
    def _get_live_contracts(self, trade_date: pd.Timestamp, symbol: str) -> pd.DataFrame:
        """Get valid contracts for trading on given date according to lifecycle rules."""
        active = self.lifecycle[(self.lifecycle["symbol"] == symbol) & 
                                (self.lifecycle["liquidity_ready"] <= trade_date) & 
                                (self.lifecycle["tender_start"] > trade_date + pd.Timedelta(days=self.settings.backtest.roll_buffer_days))]
        return active.sort_values("expiry_date")

    def run_pair(self, pair: str, z_series: pd.Series):
        """Strict day-by-day execution with lots sizing."""
        dates = sorted(z_series.dropna().index)
        leg1, leg2 = pair.split('_')
        spec1 = get_contract_spec(leg1)
        spec2 = get_contract_spec(leg2)
        
        # Hedge ratio in lots. E.g. GOLDM (10x10=100g) vs GOLDTEN (10x10=100g) => 1:1
        # GOLDM (100g) vs GOLDGUINEA (1x8=8g) => 100/8 = 12.5 => 12 vs 100 or something. 
        # Match notionals to closest whole lots.
        notional1 = spec1.lot_size * spec1.base_unit
        notional2 = spec2.lot_size * spec2.base_unit
        
        lcm_val = np.lcm(int(notional1), int(notional2))
        lcm_val // int(notional1)
        lcm_val // int(notional2)
        
        trades = []
        position = 0
        
        entry_z = self.settings.signal.z_entry
        exit_z = self.settings.signal.z_exit
        
        for i, dt in enumerate(dates[:-1]):
            # Signal generated at close of dt
            z = z_series.loc[dt]
            
            # Execute at dt_next
            dt_next = dates[i+1]
            
            if position == 0:
                if z > entry_z:
                    position = -1
                elif z < -entry_z:
                    position = 1
                    
                if position != 0:
                    trades.append({"date": dt_next, "action": "ENTER", "pos": position})
            else:
                if (position == 1 and z > -exit_z) or (position == -1 and z < exit_z):
                    position = 0
                    trades.append({"date": dt_next, "action": "EXIT", "pos": position})
                    
        return pd.DataFrame(trades)
