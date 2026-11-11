import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import yfinance as yf

from src.financial_statements import fetch_financial_statements
from src.financial_metrics import (
    get_value_for_year,
    calculate_growth,
    calculate_roe,
    calculate_debt_equity,
    calculate_net_profit_margin,
    format_financial_value
)


st.set_page_config(
    page_title="Company Comparison",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ NSE Company Comparison")
st.write("Compare two companies using fundamental analysis.")


# Normalize NSE stock tickers
def normalize_ticker(ticker):
    ticker = ticker.strip().upper()

    if ticker and not ticker.endswith(".NS"):
        ticker += ".NS"

    return ticker


# Cache downloaded financial data for one hour
@st.cache_data(ttl=3600)
def load_company(ticker):
    income, balance, cashflow = fetch_financial_statements(ticker)
    currency = yf.Ticker(ticker).info.get("financialCurrency")

    return income, balance, currency


# Retrieve dates that have valid revenue values
def available_dates(income):
    if income.empty or "TotalRevenue" not in income.index:
        return set()

    return {
        pd.Timestamp(date).date()
        for date in income.columns
        if pd.notna(income.loc["TotalRevenue", date])
    }


# Calculate a company's fundamental metrics
def company_metrics(income, balance, year, currency):

    revenue = get_value_for_year(
        income, "TotalRevenue", year
    )

    previous_revenue = get_value_for_year(
        income, "TotalRevenue", year - 1
    )

    net_income = get_value_for_year(
        income, "NetIncome", year
    )

    equity = get_value_for_year(
        balance, "StockholdersEquity", year
    )

    previous_equity = get_value_for_year(
        balance, "StockholdersEquity", year - 1
    )

    debt = get_value_for_year(
        balance, "TotalDebt", year
    )

    growth = calculate_growth(revenue, previous_revenue)
    margin = calculate_net_profit_margin(revenue, net_income)
    roe = calculate_roe(net_income, equity, previous_equity)
    debt_equity = calculate_debt_equity(debt, equity)

    raw_ratios = {
    "Revenue Growth": growth,
    "Net Profit Margin": margin,
    "ROE": roe,
    "Debt-to-Equity": debt_equity
    }

    def percent(value):
        return f"{value:.2f}%" if value is not None else "N/A"

    display_metrics = {
        "Revenue": format_financial_value(revenue, currency),
        "Net Income": format_financial_value(net_income, currency),
        "Revenue Growth": percent(growth),
        "Net Profit Margin": percent(margin),
        "ROE": percent(roe),
        "Debt-to-Equity": (
            f"{debt_equity:.2f}x"
            if debt_equity is not None else "N/A"
        )
    }
    return display_metrics, raw_ratios


# Company selection form
with st.form("comparison_form"):

    col1, col2 = st.columns(2)

    with col1:
        company_a = st.text_input("Company A", value="TCS")

    with col2:
        company_b = st.text_input("Company B", value="INFY")

    submitted = st.form_submit_button("Compare Companies")


if submitted:
    a = normalize_ticker(company_a)
    b = normalize_ticker(company_b)

    if not a or not b or a == b:
        st.warning("Enter two different valid tickers.")
    else:
        st.session_state["comparison"] = (a, b)


# Display the comparison
if "comparison" in st.session_state:

    a, b = st.session_state["comparison"]

    try:
        with st.spinner("Fetching financial statements..."):
            income_a, balance_a, currency_a = load_company(a)
            income_b, balance_b, currency_b = load_company(b)

        # Compare identical financial year-end dates
        common_dates = sorted(
            available_dates(income_a) & available_dates(income_b),
            reverse=True
        )

        if not common_dates:
            st.warning("No matching annual financial periods found.")
        else:
            selected_date = st.selectbox(
                "Select Financial Year",
                options=common_dates,
                format_func=lambda d: (
                    f"FY{d.year} (ending {d:%d %b %Y})"
                )
            )

            year = selected_date.year

            metrics_a,ratios_a = company_metrics(
                income_a, balance_a, year, currency_a
            )

            metrics_b,ratios_b = company_metrics(
                income_b, balance_b, year, currency_b
            )

            st.subheader(f"{a} vs {b}")

            comparison = pd.DataFrame({
                a: metrics_a,
                b: metrics_b
            })

            st.dataframe(comparison, use_container_width=True)

            st.subheader("Fundamental Ratio Comparison")
            ratio_names = [
                "Revenue Growth",
                "Net Profit Margin",
                "ROE"
            ]
            fig = go.Figure()

            for company, ratios in [(a, ratios_a), (b, ratios_b)]:
                values = [ratios[name] for name in ratio_names]

                fig.add_trace(go.Bar(
                    name=company,
                    x=ratio_names,
                    y=values,
                    text=[
                        f"{value:.2f}%" if value is not None else "N/A"
                        for value in values
                    ],
                    textposition="auto"
                ))

            fig.update_layout(
                title=f"{a} vs {b}",
                barmode="group",
                xaxis_title="Financial Metrics",
                yaxis_title="Percentage (%)",
                template="plotly_dark",
                height=450
            )

            st.plotly_chart(fig, use_container_width=True)

            if currency_a != currency_b:
                st.info(
                    "Companies have different financial reporting "
                    "currencies. Compare ratios directly, but do not "
                    "compare absolute amounts without conversion."
                )

            st.caption(
                "Source: Yahoo Finance via yfinance. "
                "Figures require verification against company filings."
            )

    except Exception as e:
        st.error(f"Unable to complete comparison: {e}")
