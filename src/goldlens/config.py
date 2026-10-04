import yaml
from pathlib import Path
from typing import Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).parent.parent.parent

class ContractSpec(BaseModel):
    lot_size: int
    base_unit: float
    purity: float
    expiry_window: str

class SplitsConfig(BaseModel):
    train_end: str
    val_end: str

class SignalConfig(BaseModel):
    z_window: int
    z_entry: float
    z_exit: float
    z_stop: float
    half_life_max: int

class BacktestConfig(BaseModel):
    execution_delay: int
    roll_buffer_days: int

class VerdictConfig(BaseModel):
    min_deflated_sharpe: float
    max_beta: float

class Settings(BaseSettings):
    database_path: str = str(PROJECT_ROOT / "data" / "goldlens.duckdb")
    contracts: Dict[str, ContractSpec] = {}
    splits: SplitsConfig
    signal: SignalConfig
    backtest: BacktestConfig
    verdict: VerdictConfig

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Settings":
        if config_path is None:
            config_path = PROJECT_ROOT / "config" / "default.yaml"
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

class CostConfig(BaseModel):
    rate: float
    type: Optional[str] = None

class SlippageConfig(BaseModel):
    k: float
    thin_multiplier: float

class CostsSettings(BaseModel):
    brokerage: CostConfig
    exchange_txn_charge: CostConfig
    ctt: CostConfig
    gst: CostConfig
    sebi_fee: CostConfig
    stamp_duty: CostConfig
    slippage: SlippageConfig

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "CostsSettings":
        if config_path is None:
            config_path = PROJECT_ROOT / "config" / "costs.yaml"
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

def get_settings() -> Settings:
    return Settings.load()

def get_costs() -> CostsSettings:
    return CostsSettings.load()
