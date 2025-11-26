import matplotlib
from calc_logic import parse_amount, do_math, pretty_duration
from flask import Flask, render_template, request

matplotlib.use("Agg")  # headless for Docker
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        try:
            loan = parse_amount(request.form["loan"])
            rate = float(request.form["rate"])
            term = int(request.form["term"])
            extra = float(request.form["extra"])
        except Exception:
            result = {"error": "Invalid input. Check your values."}
            return render_template("index.html", result=result)

        Bal, Mon = do_math(loan, rate, 0, term)
        Bal2, Mon2 = do_math(loan, rate, extra, term)

        payoff1 = pretty_duration(len(Mon))
        payoff2 = pretty_duration(len(Mon2))
        saved = pretty_duration(len(Mon) - len(Mon2))

        # Plot
        plt.figure(figsize=(7, 4))
        plt.title("Loan Payoff Comparison")
        plt.xlabel("Months")
        plt.ylabel("Remaining Balance ($)")
        plt.grid(True)
        plt.plot(Mon, Bal, label="Minimum Payments")
        plt.plot(Mon2, Bal2, label="With Extra")
        plt.legend()
        plt.tight_layout()
        plt.savefig("static/plot.png")
        plt.close()

        result = {
            "payoff1": payoff1,
            "payoff2": payoff2,
            "saved": saved,
            "plot": "/static/plot.png",
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
