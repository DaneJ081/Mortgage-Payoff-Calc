import matplotlib

matplotlib.use("Agg")

import base64
import io
import math
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from calc_logic import amortization_schedule, pretty_duration, format_k

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            loan = float(request.form["loan"])
            downpayment = float(request.form.get("downpayment", 0))
            rate = float(request.form["rate"])
            term = int(request.form["term"])
            pmi_rate = float(request.form.get("pmi", 0))
            extra = float(request.form["extra"])
            tax = float(request.form["tax"])
            insurance = float(request.form["insurance"])
            HOA = float(request.form.get("HOA", 0))
            repairs = float(request.form.get("repairs", 0))

            if not all(
                math.isfinite(v)
                for v in (
                    loan,
                    downpayment,
                    rate,
                    pmi_rate,
                    extra,
                    tax,
                    insurance,
                    HOA,
                    repairs,
                )
            ):
                raise ValueError("Values must be finite numbers")
            if loan <= 0:
                raise ValueError("Home price must be positive")
            if not 0 <= downpayment <= 100:
                raise ValueError("Down payment must be between 0 and 100")
            if rate < 0:
                raise ValueError("Interest rate cannot be negative")
            if term <= 0:
                raise ValueError("Loan term must be positive")
            if pmi_rate < 0:
                raise ValueError("PMI rate cannot be negative")
            if extra < 0:
                raise ValueError("Extra payment cannot be negative")
            if tax < 0 or insurance < 0 or HOA < 0 or repairs < 0:
                raise ValueError("Costs cannot be negative")
        except (ValueError, KeyError):
            return render_template("index.html", result={"error": "Invalid input"})

        # Down payment (%)
        downpayment_amount = loan * (downpayment / 100)
        loan_amount = loan - downpayment_amount

        # PMI (only if < 20% down)
        pmi = 0
        if downpayment < 20:
            pmi = (pmi_rate / 100) * loan_amount

        common_kwargs = dict(
            principal=loan_amount,
            annual_rate=rate,
            years=term,
            tax=tax,
            insurance=insurance,
            HOA=HOA,
            repairs=repairs,
            pmi=pmi,
        )

        # Minimum payment schedule
        balances_min, months_min, total_interest_min, monthly_payment = (
            amortization_schedule(extra_payment=0, **common_kwargs)
        )

        # Extra payment schedule
        balances_extra, months_extra, total_interest_extra, _ = amortization_schedule(
            extra_payment=extra, **common_kwargs
        )

        interest_saved = total_interest_min - total_interest_extra
        payoff_min = pretty_duration(len(months_min))
        payoff_extra = pretty_duration(len(months_extra))
        saved_duration = pretty_duration(len(months_min) - len(months_extra))

        # Plot
        buf = io.BytesIO()
        plt.style.use("dark_background")
        plt.figure(figsize=(7, 4))
        plt.plot(months_min, balances_min, label="Minimum Payments")
        plt.plot(months_extra, balances_extra, label="With Extra Payments")
        plt.title("Loan Payoff Comparison")
        plt.xlabel("Months")
        plt.ylabel("Remaining Balance ($)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=120)
        plt.close()
        buf.seek(0)
        plot_data_uri = "data:image/png;base64," + base64.b64encode(buf.read()).decode(
            "ascii"
        )

        result = {
            "monthlyPayment": round(monthly_payment),
            "extra": round(extra),
            "payoff1": payoff_min,
            "payoff2": payoff_extra,
            "totalInterest": format_k(total_interest_min),
            "totalInterest2": format_k(total_interest_extra),
            "interestDifference": format_k(interest_saved),
            "saved": saved_duration,
            "plot": plot_data_uri,
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # nosec B104
