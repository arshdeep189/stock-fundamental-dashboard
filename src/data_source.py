
"""Select demo or live financial data."""

import os
import yfinance as yf

from src.data_fetcher import (
    fetch_stock_data as fetch_live_history
)

from src.financial_statements import (
    fetch_financial_statements as fetch_live_statements
)

from src.demo_data import (
    get_demo_history,
    get_demo_info,
    get_demo_statements
)


# Default to safe, fictional public demo mode
MODE = os.getenv("APP_MODE", "demo").strip().lower()

if MODE not in ("demo", "live"):
    raise ValueError("APP_MODE must be 'demo' or 'live'")

DEMO_MODE = MODE == "demo"

DEFAULT_TICKER = "DEMO1" if DEMO_MODE else "TCS"


def normalize_ticker(ticker):
    ticker = ticker.strip().upper()

    if not ticker:
        return ""

    if DEMO_MODE:
        return ticker

    if not ticker.endswith(".NS"):
        ticker += ".NS"

    return ticker


def fetch_stock_data(ticker, period="1mo"):
    if DEMO_MODE:
        return get_demo_history(ticker, period)

    return fetch_live_history(ticker, period)


def fetch_financial_statements(ticker):
    if DEMO_MODE:
        return get_demo_statements(ticker)

    return fetch_live_statements(ticker)


def get_company_info(ticker):
    if DEMO_MODE:
        return get_demo_info(ticker)

    return yf.Ticker(ticker).info
