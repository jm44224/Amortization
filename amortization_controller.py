import datetime

class Amort_Controller:
    def __init__(self, amort_model, amort_view):
        self.amort_model = amort_model
        self.amort_view = amort_view
        self._dateIsLastDayOfMonth = False
        
    # never found out what NU stood for
    # this will round up the interest,
    # but only if it is more than zero 
    def calculateNU(self, nu):
        if (abs(nu) < .01):
            nu = 0
        else:
            nu *= 100
            nu = round(nu + 0.5)
            nu /= 100
        return nu

    # this is the first step of calculation
    # it will be improved in the future
    def amortize(self):
        badMonthAmount = False
        beginBalance = self.amort_model._loanAmount
        payment = 0
        principle = 0
        interest = 0
        endBalance = 0
        # this should not be needed
        # calcPayment is set to overridePayment
        if (self.amort_model._overridePayment > 0):
            paymentPlanned = self.amort_model._overridePayment
        else:
            paymentPlanned = self.amort_model._calcPayment
        for month in range(0, self.amort_model._loanMonths):
            if (payment > endBalance and endBalance > 0):
                beginBalance = endBalance
                interest = beginBalance * (self.amort_model._percent / 100) / 12
                interest = self.calculateNU(interest)
                payment = round(endBalance + interest, 2)
                principle = round(payment - interest, 2)
                endBalance = 0
            else:
                beginBalance = round(beginBalance - principle, 2)
                payment = paymentPlanned
                interest = beginBalance * (self.amort_model._percent / 100) / 12
                interest = self.calculateNU(interest)
                if (month == self.amort_model._loanMonths - 1 and self.amort_model._loanMonths != 1):
                    # 05-01-1992 jam - do not execute if months = 1
                    payment = round(beginBalance + interest, 2)
                    principle = beginBalance
                    # allow balloon payments if balance is greater than zero  11/14 jam
                    # REM IF (B@(2) > 1.1 * A@(4)) OR (B@(2) < .9 * A@(4)) THEN
                    # yes, the original code was BASIC, with poorly named variables
                    if (abs(payment - interest - endBalance) > .01):
                        print("payment: " + str(payment))
                        print("interest: " + str(interest))
                        print("end balance: " + str(endBalance))
                        raise ValueError("Payment less interest less ending balance is greater than zero.")
                else:
                    principle = round(payment - interest, 2)
                endBalance = round(beginBalance - principle, 2)
                print("month: " + str(month + 1))
                print("begin balance: " + str(beginBalance))
                print("payment: " + str(payment))
                print("interest: " + str(interest))
                print("principle: " + str(principle))
                print("end balance: " + str(endBalance))
                if (endBalance < 0):
                    raise ValueError("Ending balance is less than zero.")          

    # if percent, loan amount and number months are set
    # recalculate monthly payment
    # and calculate the entire loan
    def calculateMonthlyPayment(self):
        self.amort_model._calcPayment = 0.0
        if (self.amort_model._overridePayment > 0.0):
            self.amort_model._calcPayment = self.amort_model._overridePayment
        elif (self.amort_model._loanMonths > 0 and self.amort_model._loanAmount > 0):
            if (self.amort_model._percent == 0.0):
                self.amort_model._calcPayment = round(self.amort_model._loanAmount / self.amort_model._loanMonths, 2)
            else:
                monthlyPercent = self.amort_model._percent / 100.0 / 12.0
                self.amort_model._calcPayment = round(self.amort_model._loanAmount * (monthlyPercent / (1 - ((1 + monthlyPercent) ** (-1 * self.amort_model._loanMonths)))), 2)
        if (self.amort_model._calcPayment > 0):
            self.amortize()

    # compare response to Quit or Exit
    def CheckForQuit(self, response):
        return (response.lower()[:4] == 'quit' or response.lower()[:4] == 'exit')

    # if date can be last day of month
    # ask if all dates are on the last day of the month
    def CheckForLastDayOfMonth(self, dateEntered):
        self._dateIsLastDayOfMonth = False
        canBeLastDayOfMonth = False
        myDate = datetime.datetime.strptime(dateEntered, '%Y-%m-%d')
        if myDate.month == 2:
            if myDate.year % 4 == 0:
                canBeLastDayOfMonth = (myDate.day == 29)
            else:
                canBeLastDayOfMonth = (myDate.day == 28)
        elif myDate.month == 4 or myDate.month == 6 or myDate.month == 9 or myDate.month == 11:
            canBeLastDayOfMonth = (myDate.day == 30)
        else:
            canBeLastDayOfMonth = (myDate.day == 31)
        if canBeLastDayOfMonth == True:
            response = self.amort_view.promptUserLastDayOfMonth()
            # here response is True or False
            self._dateIsLastDayOfMonth = response

    # the main application
    # prompt user
    # perform calculations
    # display output
    def RunAmort(self):
        while True:
            self.amort_view.printValues(self.amort_model)
            response = self.amort_view.mainMenuResponse()
            if response.lower()[:1] == 'q':
                break
            elif response[:1] == '1':
                response = self.amort_view.promptUser('Enter %s' % self.amort_view.LABEL_LINE_1)
                if self.CheckForQuit(response) == True:
                    break
                self.amort_model.Title = response
            elif response[:1] == '2':
                response = self.amort_view.promptUser('Enter %s' % self.amort_view.LABEL_LINE_2)
                if self.CheckForQuit(response) == True:
                    break
                self.amort_model.StartDate = response
                if (self.amort_model.StartDate == response):
                    self.CheckForLastDayOfMonth(self.amort_model.StartDate)
            elif response[:1] == '3':
                response = self.amort_view.promptUser('Enter %s' % self.amort_view.LABEL_LINE_3)
                if self.CheckForQuit(response) == True:
                    break
                self.amort_model.Months = response
                self.calculateMonthlyPayment()
            elif response[:1] == '4':
                response = self.amort_view.promptUser('Enter %s' % self.amort_view.LABEL_LINE_4)
                if self.CheckForQuit(response) == True:
                    break
                self.amort_model.Amount = response
                self.calculateMonthlyPayment()
            elif response[:1] == '5':
                response = self.amort_view.promptUser('Enter %s' % self.amort_view.LABEL_LINE_5)
                if self.CheckForQuit(response) == True:
                    break
                self.amort_model.APR = response
                self.calculateMonthlyPayment()
            elif response[:1] == '6':
                response = self.amort_view.promptUser('Enter %s' % self.amort_view.LABEL_LINE_7)
                if self.CheckForQuit(response) == True:
                    break
                self.amort_model.Override = response
                self.calculateMonthlyPayment()
