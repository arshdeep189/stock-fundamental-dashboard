
import pytest
import pandas as pd

from src.demo_data import (
    get_demo_history,
    get_demo_statements
)


def test_demo_history_is_reproducible():
    first = get_demo_history("DEMO1", "1mo")
    second = get_demo_history("DEMO1", "1mo")

    pd.testing.assert_frame_equal(first, second)


def test_demo_financial_values():
    income, balance, cashflow = (
        get_demo_statements("DEMO1")
    )

    revenue = income.loc[
        "TotalRevenue",
        pd.Timestamp("2026-03-31")
    ]

    assert revenue == 4050 * 1e7


def test_unknown_demo_ticker():
    with pytest.raises(ValueError):
        get_demo_history("TCS.NS")
