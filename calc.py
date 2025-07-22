import customtkinter as ctk
import matplotlib.pyplot as plt


ctk.set_appearance_mode("System")    
ctk.set_default_color_theme("green")    
appWidth, appHeight = 600, 700

def on_closing():
    
    if app.winfo_exists():
        app.quit()
        app.destroy()

def do_math(loanAmount,interestRate,additionalMonthlyPayoff):
    Balances = []
    Months = []
    monthlyPayment = 536
    LoanTerm = 30
    

    Balance = loanAmount
    LoanTermMonths = LoanTerm*12
    monthlyInterestRate = interestRate/1200
    monthsToPayoff = 0
    totalMonthlyPayments = monthlyPayment +additionalMonthlyPayoff
    while Balance >0 and monthsToPayoff <601:
        if int(monthsToPayoff) >= 600:
            print("Mortgage is too large")
            return Balances,Months
        else:
            interest = monthlyInterestRate*Balance
            principal =totalMonthlyPayments -interest
            Balances.append(Balance)
            Months.append(monthsToPayoff)
            if principal >Balance:
                principal = Balance
            print(monthsToPayoff)
            Balance -=principal
            monthsToPayoff +=1

    return Balances,Months




# App Class
class App(ctk.CTk):
    # The layout of the window will be written
    # in the init function itself
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Mortgage Calc")  
        self.geometry(f"{appWidth}x{appHeight}")    


        
        self.mortgageAmountLabel = ctk.CTkLabel(self,
                                text="Mortgage amount")
        self.mortgageAmountLabel.grid(row=0, column=0,
                            padx=20, pady=20,
                            sticky="ew")

        self.mortgageAmountEntry = ctk.CTkEntry(self)
        self.mortgageAmountEntry.grid(row=0, column=1,
                            columnspan=3, padx=20,
                            pady=20, sticky="ew")

        self.interestRateLabel = ctk.CTkLabel(self, text="Interest rate")
        self.interestRateLabel.grid(row=1, column=0,
                           padx=20, pady=20,
                           sticky="ew")

        self.interestRateEntry = ctk.CTkEntry(self,
                            placeholder_text="7")
        self.interestRateEntry.grid(row=1, column=1,
                           columnspan=3, padx=20,
                           pady=20, sticky="ew")
        
        self.additionalMonthlyPaymentLabel = ctk.CTkLabel(self, text="Additional monthly payment")
        self.additionalMonthlyPaymentLabel.grid(row=2, column=0,
                           padx=20, pady=20,
                           sticky="ew")

        self.additionalMonthlyPaymentEntry = ctk.CTkEntry(self,
                            placeholder_text="100")
        self.additionalMonthlyPaymentEntry.grid(row=2, column=1,
                           columnspan=3, padx=20,
                           pady=20, sticky="ew")


        # Generate Button
        self.generateResultsButton = ctk.CTkButton(self,
                                         text="Generate Results",
                                         command=self.generateResults)
        self.generateResultsButton.grid(row=5, column=1,
                                        columnspan=2, padx=20, 
                                        pady=20, sticky="ew")

        # Text Box
        self.displayBox = ctk.CTkTextbox(self,
                                         width=200,
                                         height=100)
        self.displayBox.grid(row=6, column=0,
                             columnspan=4, padx=20,
                             pady=20, sticky="nsew")


    # This function is used to insert the 
    # details entered by users into the textbox
    def generateResults(self):

        additionalMonthlyPayoff = int(self.additionalMonthlyPaymentEntry.get())
        interestRate = int(self.interestRateEntry.get())
        mortgageAmount = int(self.mortgageAmountEntry.get())
        Balances,Months = do_math(mortgageAmount,interestRate,0)

        Balances2,Months2 = do_math(mortgageAmount,interestRate,additionalMonthlyPayoff)

        #Prevents too many lines/legends if generate pressed multiple times
        plt.close()
        plt.title ('Loan Payoff')
        plt.ylabel('Remaining Balance')
        plt.xlabel('Months')
        plt.grid()

        plt.plot(Months,Balances, label="Minimum Payments")
        plt.plot(Months2,Balances2, label = "With Additional Payments")
        plt.legend()
        plt.savefig("Plot.png")
        return additionalMonthlyPayoff

        
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
