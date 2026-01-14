# calc_logic.py


def calculate_monthly_principal_interest(principal, annual_rate, years):
    """Return pure mortgage payment (principal + interest) without fixed costs."""
    months = years * 12
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return principal / months
    return (monthly_rate * principal) / (1 - (1 + monthly_rate) ** -months)


def calculate_monthly_payment(
    principal, annual_rate, years, tax=0, insurance=0, HOA=0, repairs=0
):
    """
    Return total monthly payment including fixed monthly costs.
    Repairs is % of principal per year.
    """
    mortgage_payment = calculate_monthly_principal_interest(
        principal, annual_rate, years
    )
    fixed_costs = (
        tax / 12 + insurance / 12 + HOA / 12 + (repairs / 100) * principal / 12
    )
    return mortgage_payment + fixed_costs


def amortization_schedule(
    principal,
    annual_rate,
    extra_payment=0,
    years=30,
    tax=0,
    insurance=0,
    HOA=0,
    repairs=0,
):
    """
    Calculate amortization schedule.
    Returns:
      balances: remaining principal each month
      months_list: month numbers
      total_interest: total interest paid (rounded)
      total_payment: monthly payment including fixed costs (without extra)
    """
    balances = []
    months_list = []
    total_interest = 0.0

    monthly_rate = annual_rate / 12 / 100
    base_payment = calculate_monthly_principal_interest(principal, annual_rate, years)
    fixed_costs = (
        tax / 12 + insurance / 12 + HOA / 12 + (repairs / 100) * principal / 12
    )
    total_payment_with_extra = base_payment + fixed_costs + extra_payment

    balance = principal
    month = 0

    while balance > 0.01:
        interest = balance * monthly_rate
        principal_paid = max(
            0, min(total_payment_with_extra - fixed_costs - interest, balance)
        )
        total_interest += interest

        balances.append(balance)
        months_list.append(month)
        balance -= principal_paid
        month += 1

    total_payment = base_payment + fixed_costs
    return balances, months_list, round(total_interest), total_payment


def pretty_duration(months: int) -> str:
    """Convert months to human-readable duration."""
    years, remaining = divmod(months, 12)
    return f"{years} years" if remaining == 0 else f"{years} years {remaining} months"


def format_k(amount: float) -> str:
    """Format large amounts in thousands with 'K'."""
    return f"{round(amount / 1000)}"
