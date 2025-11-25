import customtkinter as ctk
import matplotlib.pyplot as plt
from PIL import Image
from decimal import Decimal, getcontext, ROUND_HALF_UP

# Set decimal precision higher than needed for safety
getcontext().prec = 28
CENT = Decimal("0.01")
ROUNDING = ROUND_HALF_UP

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

appWidth, appHeight = 1000, 600


def on_closing():
    if app.winfo_exists():
        app.quit()
        app.destroy()


def parse_amount(text):
    """Parse mortgage input: supports 250k, 1.5m, 300000, etc."""
    text = text.lower().replace(",", "").strip()

    if text.endswith("k"):
        return float(text[:-1]) * 1000
    if text.endswith("m"):
        return float(text[:-1]) * 1_000_000

    return float(text)


def calculate_monthly_payment_decimal(principal: Decimal, annual_rate: Decimal, years: int) -> Decimal:
    """Return amortized monthly payment as Decimal rounded to cents."""
    r = (annual_rate / Decimal("1200"))  # monthly rate decimal
    n = years * 12
    if r == 0:
        payment = (principal / Decimal(n)).quantize(CENT, rounding=ROUNDING)
        return payment
    # (r * P) / (1 - (1+r) ** -n)
    denom = (Decimal(1) - (Decimal(1) + r) ** (Decimal(-n)))
    payment = (r * principal / denom).quantize(CENT, rounding=ROUNDING)
    return payment


def do_math(loanAmount, interestRate, extraPayment, loanTermYears):
    """
    Returns balances (list of floats) and months (list of ints).
    Uses Decimal math (rounded to cents) so a loan with no extras will finish in exactly loanTermYears.
    """
    # Convert to Decimal with cents precision
    Balance = Decimal(str(loanAmount)).quantize(CENT, rounding=ROUNDING)
    annual_rate = Decimal(str(interestRate))
    extra = Decimal(str(extraPayment)).quantize(CENT, rounding=ROUNDING)
    loanTermmonths = loanTermYears * 12
    monthly_rate = (annual_rate / Decimal("1200"))

    monthly_payment = calculate_monthly_payment_decimal(Balance, annual_rate, loanTermYears)
    total_payment = (monthly_payment + extra).quantize(CENT, rounding=ROUNDING)

    balances = []
    months = []

    # 1) Do exactly loanTermmonths iterations first (so standard loan finishes in term)
    for month in range(loanTermmonths):
        if Balance <= CENT:
            break
        interest = (Balance * monthly_rate).quantize(CENT, rounding=ROUNDING)
        principal = (total_payment - interest).quantize(CENT, rounding=ROUNDING)
        if principal < Decimal("0.00"):
            principal = Decimal("0.00")
        if principal > Balance:
            principal = Balance

        balances.append(float(Balance))   # store as float for plotting
        months.append(month)

        Balance = (Balance - principal).quantize(CENT, rounding=ROUNDING)

    # 2) If paid off exactly, done. Otherwise continue with same total_payment until Balance <= 0 or cap
    extra_cap_months = 600  # safety cap to avoid infinite loop
    extra_month = 0
    while Balance > CENT and extra_month < extra_cap_months:
        interest = (Balance * monthly_rate).quantize(CENT, rounding=ROUNDING)
        principal = (total_payment - interest).quantize(CENT, rounding=ROUNDING)
        if principal < Decimal("0.00"):
            principal = Decimal("0.00")
        if principal > Balance:
            principal = Balance

        balances.append(float(Balance))
        months.append(loanTermmonths + extra_month)

        Balance = (Balance - principal).quantize(CENT, rounding=ROUNDING)
        extra_month += 1

    return balances, months


class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Mortgage Calc")
        self.geometry(f"{appWidth}x{appHeight}")

        # Mortgage amount
        ctk.CTkLabel(self, text="Mortgage amount ($)").grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.mortgageAmountEntry = ctk.CTkEntry(self, placeholder_text="250k")
        self.mortgageAmountEntry.insert(0, "250k")
        self.mortgageAmountEntry.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Interest rate
        ctk.CTkLabel(self, text="Interest rate (%)").grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.interestRateEntry = ctk.CTkEntry(self, placeholder_text="7")
        self.interestRateEntry.insert(0, "7")
        self.interestRateEntry.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Loan term
        ctk.CTkLabel(self, text="Loan term (years)").grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.loanTermEntry = ctk.CTkEntry(self, placeholder_text="30")
        self.loanTermEntry.insert(0, "30")
        self.loanTermEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Extra payment
        ctk.CTkLabel(self, text="Extra monthly payment ($)").grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        self.additionalMonthlyPaymentEntry = ctk.CTkEntry(self, placeholder_text="100")
        self.additionalMonthlyPaymentEntry.insert(0, "100")
        self.additionalMonthlyPaymentEntry.grid(row=3, column=1, columnspan=3, padx=20, pady=20, sticky="ew")

        # Generate button
        self.generateResultsButton = ctk.CTkButton(self, text="Generate Results", command=self.generateResults)
        self.generateResultsButton.grid(row=5, column=1, columnspan=2, padx=20, pady=20, sticky="ew")

        # Output display
        self.displayBox = ctk.CTkTextbox(self, width=200, height=100)
        self.displayBox.grid(row=6, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

        # Image frame
        self.imageFrame = ctk.CTkFrame(self)
        self.imageFrame.grid(row=0, column=4, rowspan=10, padx=20, pady=20)

        self.image_label = ctk.CTkLabel(self.imageFrame, text="")
        self.image_label.pack()

    def generateResults(self):

        try:
            loan = parse_amount(self.mortgageAmountEntry.get())
            rate = float(self.interestRateEntry.get())
            extra = float(self.additionalMonthlyPaymentEntry.get())
            loanTerm = int(self.loanTermEntry.get())
        except ValueError:
            self.displayBox.insert("end", "ERROR: Enter valid numbers.\n")
            return

        Bal, Mon = do_math(loan, rate, 0, loanTerm)
        Bal2, Mon2 = do_math(loan, rate, extra, loanTerm)

        def pretty_duration(months):
            years = months // 12
            remaining_months = months % 12
            return f"{years} years {remaining_months} months"

        payoff1 = pretty_duration(len(Mon))
        payoff2 = pretty_duration(len(Mon2))
        saved_months = len(Mon) - len(Mon2)
        saved_str = pretty_duration(saved_months)

        self.displayBox.delete("1.0", "end")
        self.displayBox.insert("end", f"Payoff WITHOUT extra: {payoff1}\n")
        self.displayBox.insert("end", f"Payoff WITH extra: {payoff2}\n")
        self.displayBox.insert("end", f"Time saved: {saved_str}\n")

        # Plot results
        plt.close()
        plt.figure()
        plt.title("Loan Payoff")
        plt.ylabel("Remaining Balance ($)")
        plt.xlabel("months")
        plt.grid()

        plt.plot(Mon, Bal, label="Minimum Payments")
        plt.plot(Mon2, Bal2, label="With Extra Payments")

        plt.legend()
        plt.savefig("plot.png")

        # Display plot in UI
        image = Image.open("plot.png")
        resized = ctk.CTkImage(light_image=image, size=(600, 400))

        self.image_label.configure(image=resized)
        self.image_label.image = resized


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
