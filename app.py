import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from src.data_fetcher import fetch_stock_data
from src.financial_statements import fetch_financial_statements

from src.financial_metrics import (
    get_value_for_year,
    calculate_growth,
    calculate_roe,
    calculate_debt_equity,
    calculate_net_profit_margin,
    get_display_units,
    format_financial_value,
    to_crores
)

st.set_page_config(
    page_title="Indian Stock Fundamental Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Indian Stock Fundamental Dashboard")
st.write("Explore NSE-listed companies using financial data.")

ticker_input = st.text_input(
    "Enter NSE stock ticker",
    value="TCS"
)

ticker = ticker_input.strip().upper()

period = st.selectbox(
    "Select Historical Period",
    ["1mo", "3mo", "6mo", "1y", "5y"],
    index=2
)

if ticker and not ticker.endswith(".NS"):
    ticker += ".NS"

if st.button("Analyze Stock"):
    st.session_state["show_analysis"] = True

if st.session_state.get("show_analysis", False):
    if not ticker or ticker == ".NS":
        st.warning("Please enter a valid ticker.")
    else:
        try:
            with st.spinner("Fetching stock data..."):
                history = fetch_stock_data(ticker,period)
                stock = yf.Ticker(ticker)
                info = stock.info

            if history is None or history.empty:
                st.error("No price data found for this ticker.")
            else:
                st.subheader(info.get("longName", ticker))

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Latest Close",
                    f"₹{history['Close'].iloc[-1]:,.2f}"
                )

                col2.metric(
                    "Period High",
                    f"₹{history['High'].max():,.2f}"
                )

                col3.metric(
                    "Period Low",
                    f"₹{history['Low'].min():,.2f}"
                )

                st.subheader("Recent Stock Price")

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=history.index,
                    y=history["Close"],
                    mode="lines",
                    name="Closing Price",
                    line=dict(color="#00BFFF", width=2)
                ))

                fig.update_layout(
                    title=f"{ticker} Historical Closing Price",
                    xaxis_title="Date",
                    yaxis_title="Price (INR)",
                    template="plotly_dark",
                    hovermode="x unified",
                    height=450
                )

                st.plotly_chart(fig, use_container_width=True)


                st.write(
                    "Financial Reporting Currency:",
                    info.get("financialCurrency", "Unknown")
                )

                income, balance, cashflow = fetch_financial_statements(ticker)
                st.divider()
                st.header("Financial Fundamentals")
                currency = info.get("financialCurrency")
                if income.empty:
                    st.warning("Financial statements unavailable.")
                else:
                    years = sorted(
                        {
                            col.year
                            for col in income.columns
                            if get_value_for_year(
                                income, "TotalRevenue", col.year
                            ) is not None
                        },
                        reverse=True
                    )

                    if not years:
                        st.warning("No usable annual revenue data found.")
                        st.stop()

                    # Financial year selector
                    selected_year = st.selectbox(
                        "Select Financial Year",
                        options=years,
                        format_func=lambda year: f"FY{year}",
                        key=f"financial_year_{ticker}"
                    )
                    previous_year = selected_year - 1
                    st.caption(
                        f"Financial Year Ending: {selected_year}"
                    )

                    # Extract income statement metrics
                    revenue = get_value_for_year(
                        income, "TotalRevenue", selected_year
                    )

                    previous_revenue = get_value_for_year(
                        income, "TotalRevenue", previous_year
                    )

                    net_income = get_value_for_year(
                        income, "NetIncome", selected_year
                    )

                    # Extract balance sheet metrics
                    equity = get_value_for_year(
                        balance, "StockholdersEquity", selected_year
                    )

                    previous_equity = get_value_for_year(
                        balance, "StockholdersEquity", previous_year
                    )

                    debt = get_value_for_year(
                        balance, "TotalDebt", selected_year
                    )

                    # Calculate fundamental ratios
                    profit_margin = calculate_net_profit_margin(
                        revenue, net_income
                    )

                    revenue_growth = calculate_growth(
                        revenue, previous_revenue
                    )

                    roe = calculate_roe(
                        net_income, equity, previous_equity
                    )

                    debt_equity = calculate_debt_equity(
                        debt, equity
                    )

                    # Display financial figures
                    st.subheader("Financial Overview")

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "Revenue",
                        format_financial_value(revenue, currency)
                    )

                    c2.metric(
                        "Net Income",
                        format_financial_value(net_income, currency)
                    )

                    c3.metric(
                        "Total Debt",
                        format_financial_value(debt, currency)
                    )

                    # Display ratios
                    st.subheader("Fundamental Ratios")

                    
                    r1, r2, r3, r4 = st.columns(4)

                    r1.metric(
                        "Revenue Growth",
                        f"{revenue_growth:.2f}%"
                        if revenue_growth is not None else "N/A"
                    )

                    r2.metric(
                        "Net Profit Margin",
                        f"{profit_margin:.2f}%"
                        if profit_margin is not None else "N/A"
                    )

                    r3.metric(
                        "Return on Equity",
                        f"{roe:.2f}%"
                        if roe is not None else "N/A"
                    )

                    r4.metric(
                        "Debt-to-Equity",
                        f"{debt_equity:.2f}"
                        if debt_equity is not None else "N/A"
                    )

                    # Historical financial trends
                    st.divider()
                    st.header("Historical Financial Performance")

                    currency = info.get("financialCurrency") or "Unknown"

                    divisor, unit = get_display_units(currency)
                    # Collect annual financial data
                    financial_data = []

                    for year in sorted(years):
                        annual_revenue = get_value_for_year(
                            income, "TotalRevenue", year
                        )

                        annual_profit = get_value_for_year(
                            income, "NetIncome", year
                        )

                        financial_data.append({
                            "Year": f"FY{year}",
                            "Revenue": annual_revenue / divisor
                            if annual_revenue is not None else None,
                            "Net Income": annual_profit / divisor
                            if annual_profit is not None else None
                        })

                    # Revenue chart
                    revenue_fig = go.Figure()

                    revenue_fig.add_trace(go.Bar(
                        x=[d["Year"] for d in financial_data],
                        y=[d["Revenue"] for d in financial_data],
                        name="Revenue"
                    ))

                    revenue_fig.update_layout(
                        title="Annual Revenue Trend",
                        xaxis_title="Financial Year",
                        yaxis_title=f"Revenue ({unit})",
                        template="plotly_dark"
                    )

                    st.plotly_chart(
                        revenue_fig,
                        use_container_width=True
                    )

                    # Net Income chart
                    profit_fig = go.Figure()

                    profit_fig.add_trace(go.Bar(
                        x=[d["Year"] for d in financial_data],
                        y=[d["Net Income"] for d in financial_data],
                        name="Net Income"
                    ))

                    profit_fig.update_layout(
                        title="Annual Net Income Trend",
                        xaxis_title="Financial Year",
                        yaxis_title=f"Net Income ({unit})",
                        template="plotly_dark"
                    )

                    st.plotly_chart(
                        profit_fig,
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"Could not retrieve data: {e}")
