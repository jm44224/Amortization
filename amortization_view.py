class Amort_View:

    def __init__(self):
        # initialize "constants" of line labels
        # TODO make them variables and add language support
        self.REQUIRED_DATE_FORMAT = 'YYYY-MM-DD'
        self.LABEL_LINE_1 = 'Amortization Title ....................'
        self.LABEL_LINE_2 = 'Date of First Payment (' + self.REQUIRED_DATE_FORMAT + ') ....'
        self.LABEL_LINE_3 = 'Number of Months of Loan ..............'
        self.LABEL_LINE_4 = 'Amount Borrowed .......................'
        self.LABEL_LINE_5 = 'Annual Percentage Rate ................'
        self.LABEL_LINE_6 = 'MONTHLY PAYMENT .......................'
        self.LABEL_LINE_7 = '  Override Monthly Payment ............'
        self.MENU_PROMPT = 'Enter Number To Edit Or Q to quit.'
        self.EDIT_PROMPT = 'Enter Exit Or Quit to quit.'
        self.LAST_DAY_OF_MONTH_PROMPT = 'Are all of the payments due on the last day of the month? (Yes/No)'
        self.LAST_DAY_OF_MONTH_PROMPT_YES = 'y'
        self.EDIT_PROMPT_QUIT = 'quit'
        self.EDIT_PROMPT_EXIT = 'exit'
        self.EDIT_PROMPT_ENTER = 'Enter'
        self.MENU_PROMPT_QUIT = 'q'
        self.AMORT_ERROR_END_BAL_LESS_THAN_ZERO = 'Ending balance is less than zero.'
        self.AMORT_ERROR_TOTAL_SUM_GREATER_THAN_ZERO = 'Payment less interest less ending balance is greater than zero.'
        self.DATA_ERROR_INVALID_DATE_FORMAT_CHECK = 'does not match format'
        self.DATA_ERROR_INVALID_DATE_FORMAT = 'Error: Not in required date format.'
        self.DATA_ERROR_INVALID_DATE_CHECK = 'out of range for month'
        self.DATA_ERROR_INVALID_DATE = 'Error: Not a valid date.'
        self.DATA_ERROR_INVALID_PERCENTAGE = 'Error: Not a valid percentage (0.0000 to 100.0000).'
        self.DATA_ERROR_INVALID_AMOUNT = 'Error: Not a valid amount (minimum of 0.01)'
        self.DATA_ERROR_INVALID_MONTHS = 'Error: Not a valid number of months (minimum of 1).'
        self.DATA_ERROR_INVALID_OVERRIDE = 'Error: Not a valid payment override (minimum of 0.01).'
        
    # shows all values to the user
    def printValues(self, model):
        print("(1) %s %s" % (self.LABEL_LINE_1 , model._title))
        print("(2) %s %s" % (self.LABEL_LINE_2 , model._startDate))
        print("(3) %s %d" % (self.LABEL_LINE_3 , model._loanMonths))
        print("(4) %s %.2f" % (self.LABEL_LINE_4 , model._loanAmount))
        print("(5) %s %.4f" % (self.LABEL_LINE_5 , model._percent))
        print("( ) %s %.2f" % (self.LABEL_LINE_6 , model._calcPayment))
        print("(6) %s %.2f" % (self.LABEL_LINE_7 , model._overridePayment))

    # prints current month values
    def printCurrentMonth(self, currentMonth):
        print("date: " + str(currentMonth.PaymentDate))
        print("begin balance: " + str(currentMonth.BeginBalance))
        print("payment: " + str(currentMonth.Payment))
        print("interest: " + str(currentMonth.Interest))
        print("principal: " + str(currentMonth.Principal))
        print("end balance: " + str(currentMonth.EndBalance))
                
    # prints feedback
    def printFeedback(self, msg):
        print(msg)
    
    # accepts input for any line
    def promptUserToEnter(self, msg):
        print(self.EDIT_PROMPT)        
        response = input (self.EDIT_PROMPT_ENTER + ' ' + msg + ' ')
        return response

    # prompt user last day of month
    def promptUserLastDayOfMonth(self):
        msg = self.LAST_DAY_OF_MONTH_PROMPT     
        response = input (msg + ' ')
        # return True if 'y', in case we have multiple language support
        return response.lower()[:1] == self.LAST_DAY_OF_MONTH_PROMPT_YES

    # main menu response
    def mainMenuResponse(self):
        msg = self.MENU_PROMPT   
        response = input (msg + ' ')
        return response
