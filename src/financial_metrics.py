import yfinance as yf
import pandas as pd


def get_latest_value(statement, metric):
    if statement.empty or metric not in statement.index:
        return None

    values = statement.loc[metric].dropna()

    if values.empty:
        return None

    return float(values.sort_index(ascending=False).iloc[0])



def to_crores(value, currency):
    if value is None:
        return "N/A"

    if not currency:
        return f"{value:,.2f} (currency unknown)"

    return f"{currency} {value / 1e7:,.2f} crore"



def calculate_net_profit_margin(revenue, net_income):
    if revenue is None or net_income is None or revenue == 0:
        return None

    return (net_income / revenue) * 100


def calculate_growth(current, previous):
        if current is None or previous is None or previous <= 0:
            return None

        return ((current - previous) / previous) * 100


def calculate_roe(net_income, current_equity, previous_equity):
    if any(x is None for x in
        [net_income, current_equity, previous_equity]):
        return None

    average_equity = (current_equity + previous_equity) / 2

    if average_equity <= 0:
        return None

    return (net_income / average_equity) * 100


def calculate_debt_equity(total_debt, equity):
    if total_debt is None or equity is None or equity <= 0:
        return None

    return total_debt / equity

    
def get_value_for_year(statement, metric, year):
    if statement.empty or metric not in statement.index:
        return None

    matching_columns = [
        col for col in statement.columns
        if col.year == year
    ]

    if not matching_columns:
        return None

    value = statement.loc[metric, matching_columns[0]]

    if pd.isna(value):
        return None

    return float(value)



def get_display_units(currency):
    if currency == "INR":
        return 1e7, "INR crore"

    elif currency == "USD":
        return 1e9, "USD billion"

    return 1, currency or "Unknown currency"


def format_financial_value(value, currency):
    if value is None:
        return "N/A"

    divisor, unit = get_display_units(currency)

    return f"{value / divisor:,.2f} {unit}"



if __name__ == "__main__":

    
    from src.financial_statements import fetch_financial_statements

    ticker = input("Enter NSE ticker: ").strip().upper()

    if not ticker.endswith(".NS"):
        ticker += ".NS"

    stock = yf.Ticker(ticker)
    currency = stock.info.get("financialCurrency")
    
    print("Financial Reporting Currency:", currency)

    income, balance, cashflow = fetch_financial_statements(ticker)

    revenue = get_latest_value(income, "TotalRevenue")
    net_income = get_latest_value(income, "NetIncome")
    debt = get_latest_value(balance, "TotalDebt")
    operating_cf = get_latest_value(cashflow, "OperatingCashFlow")
    free_cf = get_latest_value(cashflow, "FreeCashFlow")

    net_margin = calculate_net_profit_margin(revenue, net_income)

    print(f"\nFinancial Summary: {ticker}")
    print("-" * 40)
    print("Revenue:", to_crores(revenue, currency))
    print("Net Income:", to_crores(net_income, currency))
    print("Total Debt:", to_crores(debt, currency))
    print("Operating Cash Flow:", to_crores(operating_cf, currency))
    print("Free Cash Flow:", to_crores(free_cf, currency))

    if net_margin is not None:
        print(f"Net Profit Margin: {net_margin:.2f}%")
    else:
        print("Net Profit Margin: N/A")

    
    # Extract revenue for two financial years
    revenue_2026 = get_value_for_year(
        income, "TotalRevenue", 2026
    )

    revenue_2025 = get_value_for_year(
        income, "TotalRevenue", 2025
    )

    # Calculate revenue growth
    revenue_growth = calculate_growth(
        revenue_2026, revenue_2025
    )

    # Display result
    if revenue_growth is not None:
        print(f"Revenue Growth (FY2026 vs FY2025): {revenue_growth:.2f}%")
    else:
        print("Revenue Growth: N/A")


    
    # Extract shareholders' equity for two financial years
    equity_2026 = get_value_for_year(
        balance, "StockholdersEquity", 2026
    )

    equity_2025 = get_value_for_year(
        balance, "StockholdersEquity", 2025
    )

    # Extract total debt for FY2026
    debt_2026 = get_value_for_year(
        balance, "TotalDebt", 2026
    )

    # Extract net income for FY2026
    net_income_2026 = get_value_for_year(
        income, "NetIncome", 2026
    )

    # Calculate financial ratios
    roe = calculate_roe(
        net_income_2026, equity_2026, equity_2025
    )

    debt_equity = calculate_debt_equity(
        debt_2026, equity_2026
    )

    # Display results
    if roe is not None:
        print(f"ROE (FY2026): {roe:.2f}%")
    else:
        print("ROE: N/A")

    if debt_equity is not None:
        print(f"Debt-to-Equity (FY2026): {debt_equity:.2f}")
    else:
        print("Debt-to-Equity: N/A")



    
    

