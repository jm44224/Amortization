import datetime
from amortization_month_payment import Amort_MonthPayment
from amortization_date_functions import AddMonths
from amortization_date_functions import CanBeLastDayOfMonth

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
        endBalance = 0
        startDate = self.amort_model.StartDate
        # this should not be needed
        # calcPayment is set to overridePayment
        if (self.amort_model._overridePayment > 0):
            paymentPlanned = self.amort_model._overridePayment
        else:
            paymentPlanned = self.amort_model._calcPayment
        for month in range(0, self.amort_model._loanMonths):
            currentMonth = Amort_MonthPayment()
            currentMonth.Payment = 0
            currentMonth.Principal = 0
            currentMonth.Interest = 0
            currentMonth.EndBalance = endBalance
            currentMonth.PaymentDate = AddMonths(startDate, month, self._dateIsLastDayOfMonth)
            if (currentMonth.Payment > currentMonth.EndBalance and currentMonth.EndBalance > 0):
                currentMonth.BeginBalance = currentMonth.EndBalance
                currentMonth.Interest = currentMonth.BeginBalance * (self.amort_model._percent / 100) / 12
                currentMonth.Interest = self.calculateNU(currentMonth.Interest)
                currentMonth.Payment = round(currentMonth.EndBalance + currentMonth.Interest, 2)
                currentMonth.Principal = round(currentMonth.Payment - currentMonth.Interest, 2)
                currentMonth.EndBalance = 0
            else:
                currentMonth.BeginBalance = round(beginBalance - currentMonth.Principal, 2)
                currentMonth.Payment = paymentPlanned
                currentMonth.Interest = currentMonth.BeginBalance * (self.amort_model._percent / 100) / 12
                currentMonth.Interest = self.calculateNU(currentMonth.Interest)
                if (month == self.amort_model._loanMonths - 1 and self.amort_model._loanMonths != 1):
                    # 05-01-1992 jam - do not execute if months = 1
                    currentMonth.Payment = round(currentMonth.BeginBalance + currentMonth.Interest, 2)
                    currentMonth.Principal = currentMonth.BeginBalance
                    # allow balloon payments if balance is greater than zero  11/14 jam
                    # REM IF (B@(2) > 1.1 * A@(4)) OR (B@(2) < .9 * A@(4)) THEN
                    # yes, the original code was BASIC, with poorly named variables
                    if (abs(currentMonth.Payment - currentMonth.Interest - currentMonth.EndBalance) > .01):
                        self.amort_view.printCurrentMonth(currentMonth)
                        raise ValueError(self.amort_view.AMORT_ERROR_TOTAL_SUM_GREATER_THAN_ZERO)
                else:
                    currentMonth.Principal = round(currentMonth.Payment - currentMonth.Interest, 2)
                currentMonth.EndBalance = round(currentMonth.BeginBalance - currentMonth.Principal, 2)
                self.amort_view.printCurrentMonth(currentMonth)
                beginBalance = endBalance = currentMonth.EndBalance
                if (currentMonth.EndBalance < 0):
                    raise ValueError(self.amort_view.AMORT_ERROR_END_BAL_LESS_THAN_ZERO)          

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
        return (response.lower()[:4] == self.amort_view.EDIT_PROMPT_QUIT or response.lower()[:4] == self.amort_view.EDIT_PROMPT_EXIT)

    # if date can be last day of month
    # ask if all dates are on the last day of the month
    def CheckForLastDayOfMonth(self, dateEntered):
        self._dateIsLastDayOfMonth = False
        canBeLastDayOfMonth = CanBeLastDayOfMonth(dateEntered)
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
            if response.lower()[:1] == self.amort_view.MENU_PROMPT_QUIT:
                break
            elif response[:1] == '1':
                response = self.amort_view.promptUserToEnter(self.amort_view.LABEL_LINE_1)
                if self.CheckForQuit(response) == True:
                    break
                self.amort_model.Title = response
            elif response[:1] == '2':
                response = self.amort_view.promptUserToEnter(self.amort_view.LABEL_LINE_2)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.amort_model.StartDate = response
                    if (self.amort_model.StartDate == response):
                        self.CheckForLastDayOfMonth(self.amort_model.StartDate)
                        self.calculateMonthlyPayment()
                except ValueError as ve:
                    if ve.args[0].find(self.amort_view.DATA_ERROR_INVALID_DATE_FORMAT_CHECK) != -1:
                        self.amort_view.printFeedback(self.amort_view.DATA_ERROR_INVALID_DATE_FORMAT + ' (' + self.amort_view.REQUIRED_DATE_FORMAT + ')')
                    elif ve.args[0].find(self.amort_view.DATA_ERROR_INVALID_DATE_CHECK) != -1:
                        self.amort_view.printFeedback(slef.amort_view.DATA_ERROR_INVALID_DATE)
                    else:
                        self.amort_view.printFeedback(self.amort_view.DATA_ERROR_INVALID_DATE)
            elif response[:1] == '3':
                response = self.amort_view.promptUserToEnter(self.amort_view.LABEL_LINE_3)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.amort_model.Months = response
                    self.calculateMonthlyPayment()
                except ValueError:
                    self.amort_view.printFeedback(self.amort_view.DATA_ERROR_INVALID_MONTHS)
            elif response[:1] == '4':
                response = self.amort_view.promptUserToEnter(self.amort_view.LABEL_LINE_4)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.amort_model.Amount = response
                    self.calculateMonthlyPayment()
                except ValueError:
                    self.amort_view.printFeedback(self.amort_view.DATA_ERROR_INVALID_AMOUNT)
            elif response[:1] == '5':
                response = self.amort_view.promptUserToEnter(self.amort_view.LABEL_LINE_5)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.amort_model.APR = response
                    self.calculateMonthlyPayment()
                except ValueError:
                    self.amort_view.printFeedback(self.amort_view.DATA_ERROR_INVALID_PERCENTAGE)
            elif response[:1] == '6':
                response = self.amort_view.promptUserToEnter(self.amort_view.LABEL_LINE_7)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.amort_model.Override = response
                    self.calculateMonthlyPayment()
                except ValueError:
                    self.amort_view.printFeedback(self.amort_view.DATA_ERROR_INVALID_OVERRIDE)

