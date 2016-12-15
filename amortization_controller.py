import datetime
from amortization_month_payment import Amort_MonthPayment
from amortization_date_functions import add_months
from amortization_date_functions import CanBeLastDayOfMonth

class Amort_Controller:
    def __init__(self, amort_model, amort_view):
        self.model = amort_model
        self.view = amort_view
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
        beginBalance = self.model.Amount
        endBalance = 0
        startDate = self.model.StartDate
        # this should not be needed
        # calcPayment is set to overridePayment
        if (self.model.Override > 0):
            paymentPlanned = self.model.Override
        else:
            paymentPlanned = self.model.Payment
        for month in range(0, self.model.Months):
            currMonth = Amort_MonthPayment()
            currMonth.Payment = 0
            currMonth.Principal = 0
            currMonth.Interest = 0
            currMonth.EndBalance = endBalance
            currMonth.PaymentDate = \
                add_months(startDate, month, self._dateIsLastDayOfMonth)
            if (currMonth.Payment > currMonth.EndBalance 
                    and currMonth.EndBalance > 0):
                currMonth.BeginBalance = \
                    currMonth.EndBalance
                currMonth.Interest = (
                    currMonth.BeginBalance 
                    * (self.model.APR / 100) 
                    / 12)
                currMonth.Interest = \
                    self.calculateNU(currMonth.Interest)
                currMonth.Payment = \
                    round(currMonth.EndBalance + currMonth.Interest, 2)
                currMonth.Principal = \
                    round(currMonth.Payment - currMonth.Interest, 2)
                currMonth.EndBalance = 0
            else:
                currMonth.BeginBalance = \
                    round(beginBalance - currMonth.Principal, 2)
                currMonth.Payment = \
                    paymentPlanned
                currMonth.Interest = \
                    (currMonth.BeginBalance 
                        * (self.model.APR / 100) 
                        / 12)
                currMonth.Interest = \
                    self.calculateNU(currMonth.Interest)
                if (month == self.model.Months - 1 
                        and self.model.Months != 1):
                    # 05-01-1992 jam - do not execute if months = 1
                    currMonth.Payment = \
                        round(currMonth.BeginBalance + currMonth.Interest, 2)
                    currMonth.Principal = \
                        currMonth.BeginBalance
                    # allow balloon payments if balance is greater than zero  
                    # 11/14 jam
                    # REM IF (B@(2) > 1.1 * A@(4)) OR (B@(2) < .9 * A@(4)) THEN
                    # yes, the original code was BASIC, 
                    # with poorly named variables
                    if (abs(currMonth.Payment 
                                - currMonth.Interest 
                                - currMonth.EndBalance) > .01):
                        self.view.print_curr_month(currMonth)
                        raise ValueError(self.view.ERR_TOTAL_GT_ZERO)
                else:
                    currMonth.Principal = \
                        round(currMonth.Payment - currMonth.Interest, 2)
                currMonth.EndBalance = \
                    round(currMonth.BeginBalance - currMonth.Principal, 2)
                self.view.print_curr_month(currMonth)
                beginBalance = endBalance = currMonth.EndBalance
                if (currMonth.EndBalance < 0):
                    raise ValueError(self.view.ERR_ENDBAL_LT_ZERO)          

    # if percent, loan amount and number months are set
    # recalculate monthly payment
    # and calculate the entire loan
    def calculateMonthlyPayment(self):
        self.model.Payment = 0.0
        if (self.model.Override > 0.0):
            self.model.Payment = self.model.Override
        elif (self.model.Months > 0 
                and self.model.Amount > 0):
            if (self.model.APR == 0.0):
                self.model.Payment = \
                    round( self.model.Amount 
                            / self.model.Months
                        , 2)
            else:
                monthlyPercent = self.model.APR / 100.0 / 12.0
                self.model.Payment = \
                    round(self.model.Amount 
                            * (monthlyPercent 
                                / (1 - (
                                        (1 + monthlyPercent) 
                                            ** (-1 * self.model.Months)
                                        )
                                    )
                                )
                        , 2)
        if (self.model.Payment > 0):
            self.amortize()

    # compare response to Quit or Exit
    def CheckForQuit(self, response):
        return (response.lower()[:4] == self.view.EDIT_PROMPT_QUIT 
                or response.lower()[:4] == self.view.EDIT_PROMPT_EXIT)

    # if date can be last day of month
    # ask if all dates are on the last day of the month
    def CheckForLastDayOfMonth(self, dateEntered):
        self._dateIsLastDayOfMonth = False
        canBeLastDayOfMonth = CanBeLastDayOfMonth(dateEntered)
        if canBeLastDayOfMonth == True:
            response = self.view.user_input_is_last_day()
            # here response is True or False
            self._dateIsLastDayOfMonth = response

    # the main application
    # prompt user
    # perform calculations
    # display output
    def RunAmort(self):
        while True:
            self.view.print_menu(self.model)
            response = self.view.user_input_menu()
            if response.lower()[:1] == self.view.MENU_PROMPT_QUIT:
                break
            elif response[:1] == '1':
                response = self.view.user_input(self.view.LBL_LN_1)
                if self.CheckForQuit(response) == True:
                    break
                self.model.Title = response
            elif response[:1] == '2':
                response = self.view.user_input(self.view.LBL_LN_2)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.model.StartDate = response
                    if (self.model.StartDate == response):
                        self.CheckForLastDayOfMonth(self.model.StartDate)
                        self.calculateMonthlyPayment()
                except ValueError as ve:
                    if (ve.args[0].find(
                            self.view.ERR_INV_DATE_FORMAT_CHECK) != -1):
                        self.view.print_msg(
                            self.view.ERR_INV_DATE_FORMAT 
                            + ' (' + self.view.REQ_DATE_FMT + ')')
                    elif (ve.args[0].find(
                            self.view.ERR_INV_DATE_CHECK) != -1):
                        self.view.print_msg(self.view.ERR_INV_DATE)
                    else:
                        self.view.print_msg(self.view.ERR_INV_DATE)
            elif response[:1] == '3':
                response = self.view.user_input(self.view.LBL_LN_3)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.model.Months = response
                except ValueError:
                    self.view.print_msg(self.view.ERR_INV_MONTHS)
                    break
                self.calculateMonthlyPayment()
            elif response[:1] == '4':
                response = self.view.user_input(self.view.LBL_LN_4)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.model.Amount = response
                except ValueError:
                    self.view.print_msg(self.view.ERR_INV_AMOUNT)
                    break
                self.calculateMonthlyPayment()
            elif response[:1] == '5':
                response = self.view.user_input(self.view.LBL_LN_5)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.model.APR = response
                except ValueError:
                    self.view.print_msg(self.view.ERR_INV_PCT)
                    break
                self.calculateMonthlyPayment()
            elif response[:1] == '6':
                response = self.view.user_input(self.view.LBL_LN_7)
                if self.CheckForQuit(response) == True:
                    break
                try:
                    self.model.Override = response
                except ValueError:
                    self.view.print_msg(self.view.ERR_INV_OVERRIDE)
                    break
                self.calculateMonthlyPayment()

