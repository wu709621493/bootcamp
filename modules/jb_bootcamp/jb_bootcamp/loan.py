"""Loan repayment utilities with clear amortization math."""

from __future__ import annotations

from numbers import Number

__all__ = ["monthly_payment", "total_interest_paid"]


def _ensure_positive_number(value: Number, name: str) -> float:
    """Return ``value`` as ``float`` if positive numeric, otherwise raise."""

    if not isinstance(value, Number):
        raise TypeError(f"{name} must be numeric; got {value!r}.")
    value = float(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive; got {value}.")
    return value


def monthly_payment(
    principal: Number,
    annual_rate: Number,
    years: Number,
    payments_per_year: Number = 12,
) -> float:
    """Compute the periodic payment for a fully amortized loan.

    Parameters
    ----------
    principal
        Total amount borrowed (must be positive).
    annual_rate
        Nominal annual interest rate expressed as a fraction (e.g., 0.05 for 5%).
    years
        Length of the loan term in years.
    payments_per_year
        Number of payments made per year; defaults to monthly payments.

    Returns
    -------
    float
        The constant payment required each period to fully amortize the loan.
    """

    principal = _ensure_positive_number(principal, "principal")
    annual_rate = _ensure_positive_number(annual_rate, "annual_rate")
    years = _ensure_positive_number(years, "years")
    payments_per_year = _ensure_positive_number(payments_per_year, "payments_per_year")

    periods = int(round(years * payments_per_year))
    if periods <= 0:
        raise ValueError("Total number of payments must be at least 1.")

    rate_per_period = annual_rate / payments_per_year
    if rate_per_period == 0:
        return principal / periods

    discount_factor = 1 - (1 + rate_per_period) ** (-periods)
    if discount_factor == 0:
        raise ZeroDivisionError("Invalid parameters lead to zero discount factor.")

    return principal * rate_per_period / discount_factor


def total_interest_paid(
    principal: Number,
    annual_rate: Number,
    years: Number,
    payments_per_year: Number = 12,
) -> float:
    """Return the total interest paid over the life of the loan."""

    payment = monthly_payment(principal, annual_rate, years, payments_per_year)
    periods = int(round(float(years) * float(payments_per_year)))
    return payment * periods - float(principal)
