def calculate_monthly_principal_interest(principal, annual_rate, years):
    months = years * 12
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        return principal / months
    return (monthly_rate * principal) / (1 - (1 + monthly_rate) ** -months)


def amortization_schedule(
    principal,
    annual_rate,
    extra_payment=0,
    years=30,
    tax=0,
    insurance=0,
    HOA=0,
    repairs=0,
    pmi=0,
):
    balances = []
    months_list = []
    total_interest = 0.0

    monthly_rate = annual_rate / 12 / 100
    base_payment = calculate_monthly_principal_interest(principal, annual_rate, years)

    fixed_costs = (
        tax / 12
        + insurance / 12
        + HOA / 12
        + (repairs / 100) * principal / 12
        + pmi / 12
    )

    total_payment = base_payment + fixed_costs + extra_payment
    balance = principal
    month = 0

    while balance > 0.01:
        interest = balance * monthly_rate
        principal_paid = max(0, min(total_payment - fixed_costs - interest, balance))
        total_interest += interest
        balances.append(balance)
        months_list.append(month)
        balance -= principal_paid
        month += 1

    return balances, months_list, round(total_interest), base_payment + fixed_costs


def pretty_duration(months):
    years, rem = divmod(months, 12)
    return f"{years} years" if rem == 0 else f"{years} years {rem} months"


def format_k(amount):
    return f"{round(amount / 1000)}"
