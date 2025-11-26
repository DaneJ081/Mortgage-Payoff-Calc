def parse_amount(text):
    text = text.lower().replace(",", "").strip()
    if text.endswith("k"):
        return float(text[:-1]) * 1000
    if text.endswith("m"):
        return float(text[:-1]) * 1_000_000
    return float(text)


def calculate_monthly_payment(principal, annual_rate, years):
    r = annual_rate / 1200
    n = years * 12
    if r == 0:
        return principal / n
    return (r * principal) / (1 - (1 + r) ** (-n))


def do_math(loanAmount, interestRate, extraPayment, loanTermYears):
    Balances = []
    Months = []

    Balance = loanAmount
    monthlyInterestRate = interestRate / 1200
    monthlyPayment = calculate_monthly_payment(loanAmount, interestRate, loanTermYears)
    totalPayment = monthlyPayment + extraPayment

    month = 0
    epsilon = 0.01

    while Balance > epsilon:
        interest = Balance * monthlyInterestRate
        principal = totalPayment - interest

        if principal < 0:
            principal = 0

        if principal > Balance:
            principal = Balance

        Balances.append(Balance)
        Months.append(month)

        Balance -= principal
        month += 1

    return Balances, Months


def pretty_duration(months: int):
    years = months // 12
    remaining_months = months % 12

    if remaining_months == 0:
        return f"{years} years"
    else:
        return f"{years} years {remaining_months} months"
