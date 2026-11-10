
from src.financial_metrics import (
    calculate_growth,
    calculate_roe,
    calculate_debt_equity,
    calculate_net_profit_margin
)


def test_revenue_growth():
    result = calculate_growth(120, 100)
    assert result == 20.0


def test_net_profit_margin():
    result = calculate_net_profit_margin(1000, 200)
    assert result == 20.0


def test_roe():
    result = calculate_roe(200, 400, 600)
    assert result == 40.0


def test_debt_equity():
    result = calculate_debt_equity(250, 500)
    assert result == 0.5


def test_zero_revenue():
    result = calculate_net_profit_margin(0, 200)
    assert result is None


def test_missing_equity():
    result = calculate_debt_equity(250, None)
    assert result is None
