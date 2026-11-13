
"""Synthetic financial data for the public dashboard demo."""

import numpy as np
import pandas as pd


# Entirely fictional companies
COMPANIES = {
    "DEMO1": {
        "name": "DemoTech Ltd (Fictional)",
        "seed": 21,
        "base_price": 1450,
        "revenue": [2400, 2750, 3070, 3500, 4050],
        "profit": [280, 330, 410, 480, 560],
        "equity": [1500, 1670, 1860, 2070, 2290],
        "debt": [280, 260, 245, 230, 220],
    },
    "DEMO2": {
        "name": "DemoRetail Ltd (Fictional)",
        "seed": 42,
        "base_price": 920,
        "revenue": [3100, 3250, 3540, 3900, 4300],
        "profit": [240, 255, 295, 345, 390],
        "equity": [1950, 2100, 2260, 2450, 2660],
        "debt": [1100, 1080, 1010, 960, 940],
    },
}

PERIOD_ROWS = {
    "1mo": 22,
    "3mo": 66,
    "6mo": 132,
    "1y": 264,
    "5y": 1300,
}


def _company(ticker):
    if ticker not in COMPANIES:
        raise ValueError(
            "Demo mode supports only DEMO1 and DEMO2"
        )
    return COMPANIES[ticker]


def get_demo_info(ticker):
    data = _company(ticker)

    return {
        "longName": data["name"],
        "financialCurrency": "INR"
    }


def get_demo_history(ticker, period="1mo"):
    data = _company(ticker)

    if period not in PERIOD_ROWS:
        raise ValueError(f"Unsupported period: {period}")

    rng = np.random.default_rng(data["seed"])

    # Simulate daily returns with a fixed random seed
    returns = rng.normal(0.0003, 0.014, size=1300)

    close = data["base_price"] * np.exp(
        np.cumsum(returns)
    )

    opened = close * (
        1 + rng.normal(0, 0.004, size=1300)
    )

    high = np.maximum(opened, close) * (
        1 + rng.uniform(0, 0.01, size=1300)
    )

    low = np.minimum(opened, close) * (
        1 - rng.uniform(0, 0.01, size=1300)
    )

    history = pd.DataFrame(
        {
            "Open": opened,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": rng.integers(
                100_000, 800_000, size=1300
            ),
        },
        index=pd.bdate_range(
            end="2026-11-13",
            periods=1300
        )
    )

    history.index.name = "Date"

    return history.tail(PERIOD_ROWS[period]).copy()


def get_demo_statements(ticker):
    data = _company(ticker)

    dates = [
        pd.Timestamp(f"{year}-03-31")
        for year in range(2022, 2027)
    ]

    crore = 10_000_000

    def statement(rows):
        return pd.DataFrame(
            {
                metric: np.array(values) * crore
                for metric, values in rows.items()
            },
            index=dates
        ).T

    income = statement({
        "TotalRevenue": data["revenue"],
        "NetIncome": data["profit"]
    })

    balance = statement({
        "StockholdersEquity": data["equity"],
        "TotalDebt": data["debt"]
    })

    cashflow = statement({
        "OperatingCashFlow": [
            p * 1.35 for p in data["profit"]
        ],
        "FreeCashFlow": [
            p * 1.10 for p in data["profit"]
        ]
    })

    return income, balance, cashflow
