# 📈 Indian Stock Fundamental Analysis Dashboard

An interactive financial analytics application built using Python, Streamlit, Pandas, and Plotly to explore and compare companies listed on the National Stock Exchange of India (NSE).

## Project Overview

This project combines financial fundamental analysis with Python-based data processing and visualization.

It retrieves historical stock prices and financial statements, calculates important financial ratios, and enables side-by-side company comparisons.

## Features

### Stock Market Analysis
- Historical stock prices for NSE-listed companies
- Selectable price history (1 month to 5 years)
- Interactive Plotly price charts
- Latest closing price and period high/low

### Fundamental Analysis
- Annual revenue, net income, and debt
- Revenue growth (YoY)
- Net profit margin
- Return on Equity (ROE)
- Debt-to-Equity ratio
- Interactive financial-year selection

### Financial Visualizations
- Historical revenue and net income charts
- Side-by-side company comparison tables
- Comparative fundamental-ratio charts
- Currency-aware formatting (INR crore and USD billion)

### Data Reliability
- Exact financial reporting-date matching
- Missing-value handling
- Currency validation
- Automated unit tests using pytest
- Selected figures cross-checked against official company disclosures

## Technology Stack

**Language:** Python 3.13

**Data Processing:** Pandas, NumPy

**Financial Data:** yfinance

**Visualization:** Plotly

**Frontend:** Streamlit

**Testing:** pytest

**Version Control:** Git and GitHub

## Project Structure

```text
stock-fundamental-dashboard/
├── app.py
├── pages/
│   └── 1_Company_Comparison.py
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py
│   ├── financial_statements.py
│   ├── financial_metrics.py
│   └── data_validation.py
├── tests/
├── docs/
│   └── data_validation.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/arshdeep189/stock-fundamental-dashboard.git
cd stock-fundamental-dashboard
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, typically `http://localhost:8501`.

## Run Automated Tests

```bash
python -m pytest -v
```

**Development checkpoint:** 13 automated tests passed locally.

## Data Sources and Limitations

The local research version uses Yahoo Finance data accessed through yfinance.

Financial reporting currencies may differ between companies. The dashboard preserves source currencies instead of treating all monetary figures as INR.

Financial data can be incomplete or revised. Some accounting definitions may differ between providers and companies.

See [Financial Data Validation](docs/data_validation.md) for selected verification results and methodology.

The live-data version is intended for personal educational research. Public deployment using third-party market data is subject to the relevant data-provider permissions and terms.

## Future Improvements

- Broader financial statement verification
- More advanced company screening
- Additional industry-specific financial ratios
- Improved data-provider abstraction
- Public demonstration using appropriately licensed or permitted data

## Disclaimer

This project is for educational and research purposes only. It does not provide financial or investment advice.