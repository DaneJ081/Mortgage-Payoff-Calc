# app.py
import matplotlib

matplotlib.use("Agg")  # headless for Docker

import io
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
from calc_logic import amortization_schedule, parse_amount, pretty_duration, format_k
import os

app = Flask(__name__)
current_plot = None  # in-memory plot


@app.route("/", methods=["GET", "POST"])
def index():
    global current_plot
    result = None
    version = os.getenv("APP_VERSION", "Pre-release")

    if request.method == "POST":
        try:
            loan = parse_amount(request.form["loan"])
            rate = float(request.form["rate"])
            term = int(request.form["term"])
            extra = float(request.form["extra"])
            tax = float(request.form["tax"])
            insurance = float(request.form["insurance"])
            HOA = float(request.form.get("HOA", 0))
            repairs = float(request.form.get("repairs", 0))
        except Exception:
            result = {"error": "Invalid input. Check your values."}
            return render_template("index.html", result=result, version=version)

        # Minimum payment schedule
        balances_min, months_min, total_interest_min, monthly_payment = (
            amortization_schedule(
                principal=loan,
                annual_rate=rate,
                extra_payment=0,
                years=term,
                tax=tax,
                insurance=insurance,
                HOA=HOA,
                repairs=repairs,
            )
        )

        # Schedule with extra payments
        balances_extra, months_extra, total_interest_extra, _ = amortization_schedule(
            principal=loan,
            annual_rate=rate,
            extra_payment=extra,
            years=term,
            tax=tax,
            insurance=insurance,
            HOA=HOA,
            repairs=repairs,
        )

        # Metrics
        interest_saved = total_interest_min - total_interest_extra
        payoff_min = pretty_duration(len(months_min))
        payoff_extra = pretty_duration(len(months_extra))
        saved_duration = pretty_duration(len(months_min) - len(months_extra))

        # Generate plot
        buf = io.BytesIO()
        plt.style.use("dark_background")
        plt.figure(figsize=(7, 4))

        plt.title("Loan Payoff Comparison", color="white")
        plt.xlabel("Months", color="white")
        plt.ylabel("Remaining Balance ($)", color="white")
        plt.grid(True, color="#555")

        plt.plot(months_min, balances_min, label="Minimum Payments")
        plt.plot(months_extra, balances_extra, label="With Extra Payments")
        plt.legend(facecolor="#222", edgecolor="#444", labelcolor="white")

        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=120)
        plt.close()
        buf.seek(0)
        current_plot = buf

        # Result with interest formatted in 'K'
        result = {
            "monthlyPayment": round(monthly_payment),
            "extra": round(extra),
            "payoff1": payoff_min,
            "payoff2": payoff_extra,
            "totalInterest": format_k(total_interest_min),
            "totalInterest2": format_k(total_interest_extra),
            "interestDifference": format_k(interest_saved),
            "saved": saved_duration,
            "plot": "/plot.png",
        }

    return render_template("index.html", result=result, version=version)


@app.route("/plot.png")
def plot_png():
    if current_plot is None:
        return "No plot available", 404
    return send_file(io.BytesIO(current_plot.getvalue()), mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # nosec B104
