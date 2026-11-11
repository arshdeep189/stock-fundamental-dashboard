
import pandas as pd

from src.data_validation import (
    validate_financial_years,
    validate_currency,
    validate_ratio_inputs
)


def test_valid_financial_years():
    data = pd.DataFrame(
        {
            pd.Timestamp("2026-03-31"): [1000],
            pd.Timestamp("2025-03-31"): [900],
            pd.Timestamp("2024-03-31"): [None]
        },
        index=["TotalRevenue"]
    )

    assert validate_financial_years(data) == [2026, 2025]


def test_currency_validation():
    assert validate_currency("INR") is True
    assert validate_currency("USD") is True
    assert validate_currency("XYZ") is False


def test_valid_ratio_inputs():
    assert validate_ratio_inputs(100, 200) is True


def test_missing_ratio_inputs():
    assert validate_ratio_inputs(100, None) is False


def test_infinite_ratio_inputs():
    assert validate_ratio_inputs(100, float("inf")) is False
