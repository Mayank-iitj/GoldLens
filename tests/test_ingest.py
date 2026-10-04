import pytest
import pandas as pd
from datetime import date
from goldlens.ingest.parser import parse_bhavcopy
from goldlens.ingest.validator import validate_bhavcopy_date
import io

def test_parse_bhavcopy():
    csv_data = b"Date,Symbol,InstrumentName,ExpiryDate,Open,High,Low,Close,Volume,OpenInterest\n" \
               b"01/10/2026, GOLDM ,FUTCOM,05DEC2026,75000,75500,74900,75200,1000,5000\n"
    df = parse_bhavcopy(io.BytesIO(csv_data), ["GOLDM"])
    assert not df.empty
    assert df.iloc[0]["Symbol"] == "GOLDM"
    assert df.iloc[0]["Close"] == 75200.0

def test_validator_mismatch():
    csv_data = b"Date,Symbol\n02/10/2026,GOLDM\n"
    df = pd.read_csv(io.BytesIO(csv_data))
    df = validate_bhavcopy_date(df, date(2026, 10, 1)) # requesting 1st, got 2nd
    assert df.empty # should discard
