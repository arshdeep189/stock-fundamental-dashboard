import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from src.data_fetcher import fetch_stock_data

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

        except Exception as e:
            st.error(f"Could not retrieve data: {e}")
