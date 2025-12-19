"""Tests for loan repayment utilities."""

from __future__ import annotations

import math

import pytest

from jb_bootcamp.loan import monthly_payment, total_interest_paid


def test_monthly_payment_matches_hand_calc():
    # Example: $200,000 mortgage, 5% annual rate, 30 years, monthly payments
    payment = monthly_payment(200_000, 0.05, 30, payments_per_year=12)
    assert math.isclose(payment, 1073.64, rel_tol=0, abs_tol=0.01)


def test_zero_rate_reduces_to_simple_division():
    payment = monthly_payment(12_000, 0.0000001, 1, payments_per_year=12)
    assert math.isclose(payment, 1000, rel_tol=0, abs_tol=1e-2)


def test_total_interest_over_life_of_loan():
    interest = total_interest_paid(10_000, 0.06, 2, payments_per_year=12)
    assert interest > 0
    assert math.isclose(interest, 636.95, rel_tol=0, abs_tol=0.1)


@pytest.mark.parametrize(
    "principal, rate, years, msg",
    [
        (0, 0.05, 10, "principal must be positive"),
        (1000, -0.01, 5, "annual_rate must be positive"),
        (1000, 0.05, 0, "years must be positive"),
        (1000, 0.05, 5, "payments_per_year must be positive"),
    ],
)
def test_invalid_inputs_raise(principal, rate, years, msg):
    with pytest.raises((TypeError, ValueError)) as excinfo:
        monthly_payment(principal, rate, years, payments_per_year=0)
    assert msg.split()[0] in str(excinfo.value)
