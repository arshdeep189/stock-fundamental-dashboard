# Indian Stock Fundamental Analysis Dashboard

A Python-based financial analysis project for analysing Indian stock market companies listed on the NSE.

## Project Objectives
- Retrieve historical stock prices and company financial statements.
- Calculate fundamental financial ratios.
- Compare companies based on financial performance.
- Build an interactive dashboard using Streamlit.

## Technologies
Python, Pandas, NumPy, yfinance, Streamlit, Plotly, pytest, Git.

## Implemented Features
- NSE stock data retrieval
- Annual income statement, balance sheet and cash flow retrieval
- Net profit margin calculation
- Year-over-year revenue growth
- Return on equity (ROE)
- Debt-to-equity ratio
- Automated unit tests

## Installation

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Activate the virtual environment before installing dependencies.

## Running the Project

```bash
python -m src.financial_metrics
```

## Running Tests

```bash
python -m pytest -v
```

## Project Status

**In development.** An interactive dashboard, financial visualizations and company comparisons are planned.

## Disclaimer

This project is for educational and research purposes only, not financial advice. Third-party market data may be incomplete or inaccurate.