class AmortizationView:

    def __init__(self):
        # initialize "constants" of line labels
        # TODO make them variables and add language support
        self.REQ_DATE_FMT = 'YYYY-MM-DD'
        self.LBL_LN_1 = 'Amortization Title ....................'
        self.LBL_LN_2 = 'Date of First Payment (' + self.REQ_DATE_FMT + ') ....'
        self.LBL_LN_3 = 'Number of Months of Loan ..............'
        self.LBL_LN_4 = 'Amount Borrowed .......................'
        self.LBL_LN_5 = 'Annual Percentage Rate ................'
        self.LBL_LN_6 = 'MONTHLY PAYMENT .......................'
        self.LBL_LN_7 = '  Override Monthly Payment ............'
        self.MENU_PROMPT = 'Enter Number To Edit, P to print, Q to quit.'
        self.EDIT_PROMPT = 'Enter Exit Or Quit to quit.'
        self.LAST_DAY_MONTH = 'Are all of the payments due on the last day of the month? (Yes/No)'
        self.LAST_DAY_MONTH_YES = 'y'
        self.EDIT_PROMPT_QUIT = 'quit'
        self.EDIT_PROMPT_EXIT = 'exit'
        self.EDIT_PROMPT_ENTER = 'Enter'
        self.MENU_PROMPT_QUIT = 'q'
        self.MENU_PROMPT_PRINT = 'p'
        self.ERR_END_BAL_LT_ZERO = 'Ending balance is less than zero.'
        self.ERR_TOTAL_GT_ZERO = 'Payment less interest less ending balance is greater than zero.'
        self.ERR_INV_DATE_FORMAT_CHECK = 'does not match format'
        self.ERR_INV_DATE_FORMAT = 'Error: Not in required date format.'
        self.ERR_INV_DATE_CHECK = 'out of range for month'
        self.ERR_INV_DATE = 'Error: Not a valid date.'
        self.ERR_INV_PCT = 'Error: Not a valid percentage (0.0000 to 100.0000).'
        self.ERR_INV_AMOUNT = 'Error: Not a valid amount (minimum of 0.01)'
        self.ERR_INV_MONTHS = 'Error: Not a valid number of months (minimum of 1).'
        self.ERR_INV_OVERRIDE = 'Error: Not a valid payment override (minimum of 0.01).'
        
    # shows all values to the user
    def print_menu(self, model):
        print("  (1) %s %s" % (self.LBL_LN_1, model.title))
        print("  (2) %s %s" % (self.LBL_LN_2, model.start_date))
        print("  (3) %s %d" % (self.LBL_LN_3, model.loan_months))
        print("  (4) %s %.2f" % (self.LBL_LN_4, model.loan_amount))
        print("  (5) %s %.4f" % (self.LBL_LN_5, model.annual_percentage_rate))
        print("  ( ) %s %.2f" % (self.LBL_LN_6, model.calculated_payment))
        print("  (6) %s %.2f" % (self.LBL_LN_7, model.override_payment))


    @staticmethod
    def print_output_header():
        print("PAYMENT DATE   BEGIN BAL     PAYMENT    INTEREST   PRINCIPAL     END BAL")

    @staticmethod
    def print_output_footer(total_payments, total_interest, total_principal):
        print("                         " +
              f"{total_payments:11.2f} " +
              f"{total_interest:11.2f} " +
              f"{total_principal:11.2f}")

    # prints current month values
    @staticmethod
    def print_curr_month(current_month):
        print(f"  {str(current_month.payment_date)} " +
              f"{current_month.beginning_balance:11.2f} " +
              f"{current_month.calculated_payment:11.2f} " +
              f"{current_month.interest:11.2f} " +
              f"{current_month.principal:11.2f} " +
              f"{current_month.ending_balance:11.2f}")

    # accepts input for any line
    def user_input(self, msg):
        print(self.EDIT_PROMPT)        
        return input (self.EDIT_PROMPT_ENTER + ' ' + msg + ' ')

    # prompt user last day of month
    def user_input_is_last_day(self):
        response = input(self.LAST_DAY_MONTH + ' ')
        # return True if 'y', in case we have multiple language support
        return response.lower()[:1] == self.LAST_DAY_MONTH_YES

    # main menu response
    def user_input_menu(self):
        return input(self.MENU_PROMPT + ' ')
