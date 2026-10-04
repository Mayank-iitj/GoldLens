from ..config import get_settings, ContractSpec

def get_contract_spec(symbol: str) -> ContractSpec:
    settings = get_settings()
    if symbol not in settings.contracts:
        raise ValueError(f"Unknown contract {symbol}")
    return settings.contracts[symbol]
