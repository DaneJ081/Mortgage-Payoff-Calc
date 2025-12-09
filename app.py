import matplotlib
matplotlib.use("Agg")  # headless for Docker
import matplotlib.pyplot as plt
import io
from flask import Flask, render_template, request, send_file
from calc_logic import parse_amount, do_math, pretty_duration

app = Flask(__name__)

# Store the plot in-memory for the current calculation
current_plot = None

@app.route("/", methods=["GET", "POST"])
def index():
    global current_plot
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

        # Calculate balances
        Bal, Mon, totalInterest = do_math(loan, rate, 0, term)
        Bal2, Mon2, totalInterest2 = do_math(loan, rate, extra, term)

        interestDifference = totalInterest - totalInterest2
        payoff1 = pretty_duration(len(Mon))
        payoff2 = pretty_duration(len(Mon2))
        saved = pretty_duration(len(Mon) - len(Mon2))

        # Generate plot in-memory (dark mode)
        buf = io.BytesIO()
        plt.style.use("dark_background")
        plt.figure(figsize=(7, 4))

        plt.title("Loan Payoff Comparison", color="white")
        plt.xlabel("Months", color="white")
        plt.ylabel("Remaining Balance ($)", color="white")

        plt.grid(True, color="#555")  # softer gray grid

        plt.plot(Mon, Bal, label="Minimum Payments")
        plt.plot(Mon2, Bal2, label="With Extra")

        plt.legend(facecolor="#222", edgecolor="#444", labelcolor="white")

        plt.tight_layout()
        plt.savefig(buf, format="png", dpi=120)
        plt.close()
        buf.seek(0)
        current_plot = buf

        result = {
            "payoff1": payoff1,
            "payoff2": payoff2,
            "totalInterest": totalInterest,
            "totalInterest2": totalInterest2,
            "interestDifference": interestDifference,
            "saved": saved,
            "plot": "/plot.png",  # points to new route
        }

    return render_template("index.html", result=result)

@app.route("/plot.png")
def plot_png():
    if current_plot is None:
        return "No plot available", 404
    # Return a copy of the BytesIO object
    return send_file(io.BytesIO(current_plot.getvalue()), mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
