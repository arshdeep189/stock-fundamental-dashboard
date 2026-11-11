
import pandas as pd


def validate_financial_years(statement):
    """Return years with valid annual revenue data."""
    if statement.empty or "TotalRevenue" not in statement.index:
        return []

    valid_years = []

    for col in statement.columns:
        value = statement.loc["TotalRevenue", col]

        if pd.notna(value):
            valid_years.append(col.year)

    return sorted(set(valid_years), reverse=True)


def validate_currency(currency):
    """Check whether a reporting currency is supported."""
    return currency in ("INR", "USD")


def validate_ratio_inputs(*values):
    """Check that all inputs are present and finite."""
    return all(
        value is not None
        and pd.notna(value)
        and pd.api.types.is_number(value)
        and float("-inf") < value < float("inf")
        for value in values
    )

