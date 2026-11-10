import yfinance as yf


def fetch_stock_data(ticker,period="1mo"):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    if history.empty:
        return None

    return history


if __name__ == "__main__":
    ticker = input("Enter NSE stock ticker (e.g. TCS): ").strip().upper()

    if not ticker.endswith(".NS"):
        ticker += ".NS"

    history = fetch_stock_data(ticker)

    if history is None:
        print("No stock data found!")
    else:
        print(f"\nStock: {ticker}")
        print(f"Latest Closing Price: Rs. {history['Close'].iloc[-1]:.2f}")
        print(f"5-Day High: Rs. {history['High'].max():.2f}")
        print(f"5-Day Low: Rs. {history['Low'].min():.2f}")
        print(f"Average Close: Rs. {history['Close'].mean():.2f}")
