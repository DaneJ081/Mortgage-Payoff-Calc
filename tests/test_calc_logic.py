# tests/test_calc_logic.py
import pytest
from calc_logic import (
    calculate_monthly_principal_interest,
    calculate_monthly_payment,
    amortization_schedule,
    pretty_duration,
    format_k,
)


def test_zero_interest():
    principal = 12_000
    annual_rate = 0
    years = 10
    payment = calculate_monthly_principal_interest(principal, annual_rate, years)
    assert payment == 100  # 12,000 / 12*12 months


# ------------------------
# Test calculate_monthly_payment (includes fixed costs)
# ------------------------
def test_monthly_payment_with_fixed_costs():
    principal = 100_000
    annual_rate = 5
    years = 30
    tax = 3600  # annual
    insurance = 1200
    HOA = 600
    repairs = 1  # 1% of principal per year

    payment = calculate_monthly_payment(
        principal, annual_rate, years, tax, insurance, HOA, repairs
    )
    assert payment > 0


# ------------------------
# Test amortization_schedule
# ------------------------
def test_amortization_schedule_basic():
    principal = 50_000
    annual_rate = 4
    years = 15

    balances, months, total_interest, monthly_payment = amortization_schedule(
        principal, annual_rate, years=years
    )
    assert balances[0] == principal
    assert len(months) > 0
    assert total_interest > 0
    assert monthly_payment > 0
    # Number of months should be roughly years * 12
    assert abs(len(months) - (years * 12)) <= 1


def test_amortization_schedule_extra_payment_reduces_term():
    principal = 100_000
    annual_rate = 5
    years = 30
    extra_payment = 200

    balances_min, months_min, _, _ = amortization_schedule(
        principal, annual_rate, 0, years
    )
    balances_extra, months_extra, _, _ = amortization_schedule(
        principal, annual_rate, extra_payment, years
    )

    # Extra payments reduce number of months
    assert len(months_extra) < len(months_min)
    # Total interest with extra payment is lower
    _, _, total_interest_min, _ = amortization_schedule(
        principal, annual_rate, 0, years
    )
    _, _, total_interest_extra, _ = amortization_schedule(
        principal, annual_rate, extra_payment, years
    )
    assert total_interest_extra < total_interest_min


# ------------------------
# Test pretty_duration
# ------------------------
@pytest.mark.parametrize(
    "months, expected", [(12, "1 years"), (25, "2 years 1 months"), (0, "0 years")]
)
def test_pretty_duration(months, expected):
    assert pretty_duration(months) == expected


# ------------------------
# Test format_k
# ------------------------
@pytest.mark.parametrize("amount, expected", [(1200, "1"), (999_999, "1000"), (0, "0")])
def test_format_k(amount, expected):
    assert format_k(amount) == expected
