import datetime
from amortization_month_payment import AmortizationMonthPayment
from amortization_date_functions import add_months
from amortization_date_functions import can_be_last_day_of_month


class AmortizationController:
    payment_list = []

    def __init__(self, amortization_model, amortization_view):
        self.model = amortization_model
        self.view = amortization_view
        self._dateIsLastDayOfMonth = False

    # never found out what NU stood for
    # this will round up the interest,
    # but only if it is more than zero
    @staticmethod
    def calculate_nu(nu):
        if abs(nu) < .01:
            nu = 0
        else:
            nu *= 100
            nu = round(nu + 0.5)
            nu /= 100
        return nu

    # this is the first step of calculation
    # it will be improved in the future
    def amortize(self):
        self.payment_list.clear()
        beginning_balance = self.model.loan_amount
        ending_balance = 0
        start_date = self.model.start_date
        # this should not be needed
        # calcPayment is set to overridePayment
        if self.model.override_payment > 0:
            payment_planned = self.model.override_payment
        else:
            payment_planned = self.model.calculated_payment
        for month in range(0, self.model.loan_months):
            current_month = AmortizationMonthPayment()
            current_month.calculated_payment = 0
            current_month.principal = 0
            current_month.interest = 0
            current_month.ending_balance = ending_balance
            current_month.payment_date = \
                add_months(start_date, month, self._dateIsLastDayOfMonth)
            if current_month.calculated_payment > current_month.ending_balance > 0:
                current_month.beginning_balance = \
                    current_month.ending_balance
                current_month.interest = (
                        current_month.beginning_balance
                        * (self.model.annual_percentage_rate / 100)
                        / 12)
                current_month.interest = \
                    self.calculate_nu(current_month.interest)
                current_month.calculated_payment = \
                    round(current_month.ending_balance + current_month.interest, 2)
                current_month.principal = \
                    round(current_month.calculated_payment - current_month.interest, 2)
                current_month.ending_balance = 0
            else:
                current_month.beginning_balance = \
                    round(beginning_balance - current_month.principal, 2)
                current_month.calculated_payment = \
                    payment_planned
                current_month.interest = \
                    (current_month.beginning_balance
                     * (self.model.annual_percentage_rate / 100)
                     / 12)
                current_month.interest = \
                    self.calculate_nu(current_month.interest)
                if (month == self.model.loan_months - 1
                        and self.model.loan_months != 1):
                    # 05-01-1992 jam - do not execute if months = 1
                    current_month.calculated_payment = \
                        round(current_month.beginning_balance + current_month.interest, 2)
                    current_month.principal = \
                        current_month.beginning_balance
                    # allow balloon payments if balance is greater than zero  
                    # 11/14 jam
                    # REM IF (B@(2) > 1.1 * A@(4)) OR (B@(2) < .9 * A@(4)) THEN
                    # yes, the original code was BASIC, 
                    # with poorly named variables
                    if (abs(current_month.calculated_payment
                            - current_month.interest
                            - current_month.ending_balance) > .01):
                        self.payment_list.append(current_month)
                        raise ValueError(self.view.ERR_TOTAL_GT_ZERO)
                else:
                    current_month.principal = \
                        round(current_month.calculated_payment - current_month.interest, 2)
                current_month.ending_balance = \
                    round(current_month.beginning_balance - current_month.principal, 2)
                self.payment_list.append(current_month)
                beginning_balance = ending_balance = current_month.ending_balance
                if current_month.ending_balance < 0:
                    raise ValueError(self.view.ERR_ENDBAL_LT_ZERO)

                    # if percent, loan amount and number months are set

    # recalculate monthly payment
    # and calculate the entire loan
    def calculate_monthly_payment(self):
        self.model.calculated_payment = 0.0
        if self.model.override_payment > 0.0:
            self.model.calculated_payment = self.model.override_payment
        elif self.model.loan_months > 0 and self.model.loan_amount > 0:
            if self.model.annual_percentage_rate == 0.0:
                self.model.calculated_payment = round(self.model.loan_amount / self.model.loan_months, 2)
            else:
                monthly_percent = self.model.annual_percentage_rate / 100.0 / 12.0
                self.model.calculated_payment = \
                    round(self.model.loan_amount *
                          (monthly_percent / (1 - ((1 + monthly_percent) ** (-1 * self.model.loan_months)))), 2)
        if self.model.calculated_payment > 0:
            self.amortize()

    # compare response to Quit or Exit
    def check_for_quit(self, response):
        return (response.lower()[:4] == self.view.EDIT_PROMPT_QUIT
                or response.lower()[:4] == self.view.EDIT_PROMPT_EXIT)

    # if date can be last day of month
    # ask if all dates are on the last day of the month
    def check_for_last_day_of_month(self, date_entered):
        self._dateIsLastDayOfMonth = False
        if can_be_last_day_of_month(date_entered):
            response = self.view.user_input_is_last_day()
            # here response is True or False
            self._dateIsLastDayOfMonth = response

    # the main application
    # prompt user
    # perform calculations
    # display output
    def run_amortization(self):
        while True:
            self.view.print_menu(self.model)
            response = self.view.user_input_menu().lower()[:1]
            if response == self.view.MENU_PROMPT_QUIT:
                break
            elif response == self.view.MENU_PROMPT_PRINT:
                self.view.print_output_header()
                total_payments = 0
                total_interest = 0
                total_principal = 0
                for i in range(len(self.payment_list)):
                    total_payments += self.payment_list[i].calculated_payment
                    total_interest += self.payment_list[i].interest
                    total_principal += self.payment_list[i].principal
                    self.view.print_curr_month(self.payment_list[i])
                self.view.print_output_footer(total_payments, total_interest, total_principal)
            elif response == '1':
                response = self.view.user_input(self.view.LBL_LN_1)
                if self.check_for_quit(response):
                    break
                self.model.title = response
            elif response == '2':
                response = self.view.user_input(self.view.LBL_LN_2)
                if self.check_for_quit(response):
                    break
                try:
                    self.model.start_date = response
                    if self.model.start_date == response:
                        self.check_for_last_day_of_month(self.model.start_date)
                        self.calculate_monthly_payment()
                except ValueError as ve:
                    if ve.args[0].find(self.view.ERR_INV_DATE_FORMAT_CHECK) != -1:
                        print(self.view.ERR_INV_DATE_FORMAT + ' (' + self.view.REQ_DATE_FMT + ')')
                    elif ve.args[0].find(self.view.ERR_INV_DATE_CHECK) != -1:
                        print(self.view.ERR_INV_DATE)
                    else:
                        print(self.view.ERR_INV_DATE)
            elif response == '3':
                response = self.view.user_input(self.view.LBL_LN_3)
                if self.check_for_quit(response):
                    break
                try:
                    self.model.loan_months = response
                except ValueError:
                    print(self.view.ERR_INV_MONTHS)
                self.calculate_monthly_payment()
            elif response == '4':
                response = self.view.user_input(self.view.LBL_LN_4)
                if self.check_for_quit(response):
                    break
                try:
                    self.model.loan_amount = response
                except ValueError:
                    print(self.view.ERR_INV_AMOUNT)
                self.calculate_monthly_payment()
            elif response == '5':
                response = self.view.user_input(self.view.LBL_LN_5)
                if self.check_for_quit(response):
                    break
                try:
                    self.model.annual_percentage_rate = response
                except ValueError:
                    print(self.view.ERR_INV_PCT)
                self.calculate_monthly_payment()
            elif response == '6':
                response = self.view.user_input(self.view.LBL_LN_7)
                if self.check_for_quit(response):
                    break
                try:
                    self.model.override_payment = response
                except ValueError:
                    print(self.view.ERR_INV_OVERRIDE)
                self.calculate_monthly_payment()
