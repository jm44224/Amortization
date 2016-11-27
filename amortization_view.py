class Amort_View:

    def __init__(self):
        # initialize "constants" of line labels
        self.LABEL_LINE_1 = 'Amortization Title ....................'
        self.LABEL_LINE_2 = 'Date of First Payment (YYYY-MM-DD) ....'
        self.LABEL_LINE_3 = 'Number of Months of Loan ..............'
        self.LABEL_LINE_4 = 'Amount Borrowed .......................'
        self.LABEL_LINE_5 = 'Annual Percentage Rate ................'
        self.LABEL_LINE_6 = 'MONTHLY PAYMENT .......................'
        self.LABEL_LINE_7 = '  Override Monthly Payment ............'

    # shows all values to the user
    def printValues(self, model):
        print("(1) %s %s" % (self.LABEL_LINE_1 , model._title))
        print("(2) %s %s" % (self.LABEL_LINE_2 , model._startDate))
        print("(3) %s %d" % (self.LABEL_LINE_3 , model._loanMonths))
        print("(4) %s %.2f" % (self.LABEL_LINE_4 , model._loanAmount))
        print("(5) %s %.4f" % (self.LABEL_LINE_5 , model._percent))
        print("( ) %s %.2f" % (self.LABEL_LINE_6 , model._calcPayment))
        print("(6) %s %.2f" % (self.LABEL_LINE_7 , model._overridePayment))

    # accepts input for any line
    def promptUser(self, msg):
        print ('Enter Exit Or Quit to quit.  ')        
        response = input (msg + ' ')
        return response

    # prompt user last day of month
    def promptUserLastDayOfMonth(self):
        msg = 'Are all of the payments due on the last day of the month? (Yes/No)  '     
        response = input (msg + ' ')
        # return True if 'y', in case we have multiple language support
        return response.lower()[:1] == 'y'

    # main menu response
    def mainMenuResponse(self):
        response = input ('Enter Number To Edit Or Q to quit.  ')
        return response
