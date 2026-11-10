import yfinance as yf


def fetch_financial_statements(ticker):
    stock = yf.Ticker(ticker)

    income = stock.get_income_stmt(freq="yearly")
    balance = stock.get_balance_sheet(freq="yearly")
    cashflow = stock.get_cash_flow(freq="yearly")

    return income, balance, cashflow


if __name__ == "__main__":
    ticker = input("Enter NSE ticker: ").strip().upper()

    if not ticker.endswith(".NS"):
        ticker += ".NS"

    income, balance, cashflow = fetch_financial_statements(ticker)

    print("\n========== INCOME STATEMENT ==========")
    print(income if not income.empty else "Data unavailable")

    print("\n========== BALANCE SHEET ==========")
    print(balance if not balance.empty else "Data unavailable")

    print("\n========== CASH FLOW STATEMENT ==========")
    print(cashflow if not cashflow.empty else "Data unavailable")

# if not income.empty and "Total Revenue" in income.index:
#     revenue = income.loc["Total Revenue"]
#     print("\nAnnual Revenue:")
#     print(revenue)