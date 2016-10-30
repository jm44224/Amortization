
import datetime

class Amort:
    def __init__ (self):
        # initialize variables
        self._title = ""
        self._startDate = datetime.date.today()
        self._loanMonths = 0
        self._loanAmount = 0.00
        self._percent = 0.0000
        self._calcPayment = 0.00
        self._overridePayment = 0.00
        # initialize "constants" of line labels
        self.LABEL_LINE_1 = 'Amortization Title ....................'
        self.LABEL_LINE_2 = 'Date of First Payment (YYYY-MM-DD) ....'
        self.LABEL_LINE_3 = 'Number of Months of Loan ..............'
        self.LABEL_LINE_4 = 'Amount Borrowed .......................'
        self.LABEL_LINE_5 = 'Annual Percentage Rate ................'
        self.LABEL_LINE_6 = 'MONTHLY PAYMENT .......................'
        self.LABEL_LINE_7 = '  Override Monthly Payment ............'

    # get / set Loan Amount, validate as a positive number
    # recalculate monthly payment if set
    @property
    def Amount(self):
        return self._loanAmount
    @Amount.setter
    def Amount(self, value):
        if float(value) >=0.01:
            self._loanAmount  = round(float(value), 2)
            self.calculateMonthlyPayment()
        else:
            print(str(value) + " is not a valid number for amount (minimum of 0.01).")

    # get / set Annual Percentage Rate, validate as a positive percentage
    # recalculate monthly payment if set            
    @property
    def APR(self):
        return self._percent
    @APR.setter
    def APR(self, value):
        if float(value) >=0.0 and float(value) <=100.0:
            value = round(float(value), 4)
            self._percent = float(value)
            self.calculateMonthlyPayment()
        else:
            print(str(value) + " is not a valid number for percentage (0.0000 to 100.0000).")

    # get / set Months of Loan, validate as a positive integer
    # recalculate monthly payment if set            
    @property
    def Months(self):
        return self._loanMonths
    @Months.setter
    def Months(self, value):
        if int(value) >=1:
            self._loanMonths = int(value)
            self.calculateMonthlyPayment()
        else:
            print(str(value) + " is not a valid number for months (minimum of 1).")

    # get / set Monthly Payment Override, validate as a positive number
    # recalculate monthly payment if set
    @property
    def Override(self):
        return self._overridePayment
    @Override.setter
    def Override(self, value):
        if float(value) >=0.01:
            self._overridePayment  = round(float(value), 2)
            self.calculateMonthlyPayment()
        else:
            print(str(value) + " is not a valid number for payment override (minimum of 0.01).")

    # get / set Start Date of Payment, validate as a valid date format
    # this is not yet used            
    @property
    def StartDate(self):
        return self._startDate
    @StartDate.setter
    def StartDate(self, value):
        if self.validateDate(value) == True:
            self._startDate = value
        else:
            print(str(value) + " is not a valid start date (YYYY-MM-DD).")

    # get / set Loan Title
    # this is not yet used    
    @property
    def Title(self):
        return self._title
    @Title.setter
    def Title(self, value):
        self._title = str(value)

    # if percent, loan amount and number months are set
    # recalculate monthly payment
    def calculateMonthlyPayment(self):
        self._calcPayment = 0.0
        if (self._overridePayment > 0.0):
            self._calcPayment = self._overridePayment
        elif (self._loanMonths > 0 and self._loanAmount > 0):
            if (self._percent == 0.0):
                self._calcPayment = round(self._loanAmount / self._loanMonths, 2)
            else:
                monthlyPercent = self._percent / 100.0 / 12.0
                self._calcPayment = round(self._loanAmount * (monthlyPercent / (1 - ((1 + monthlyPercent) ** (-1 * self._loanMonths)))), 2)

    # shows all values to the user
    def printValues(self):
        print("(1) %s %s" % (self.LABEL_LINE_1 , self._title))
        print("(2) %s %s" % (self.LABEL_LINE_2 , self._startDate))
        print("(3) %s %d" % (self.LABEL_LINE_3 , self._loanMonths))
        print("(4) %s %.2f" % (self.LABEL_LINE_4 , self._loanAmount))
        print("(5) %s %.4f" % (self.LABEL_LINE_5 , self._percent))
        print("( ) %s %.2f" % (self.LABEL_LINE_6 , self._calcPayment))
        print("(6) %s %.2f" % (self.LABEL_LINE_7 , self._overridePayment))

    # accepts input for any line
    def promptUser(self, msg):
        print ('Enter Exit Or Quit to quit.  ')        
        response = input (msg + ' ')
        return response

    # validates that a given date is in the correct format
    # validates that a given date is actually a date
    def validateDate(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError as ve:
            if ve.args[0].find('does not match format') != -1:
                print("You must enter a date in the format of YYYY-MM-DD.")
            elif ve.args[0].find('out of range for month') != -1:
                print("You must enter a valid date.")
        return False


amort = Amort()
while True:
    amort.printValues()
    response = input ('Enter Number To Edit Or Q to quit.  ')
    if response.lower()[:1] == 'q':
        break
    elif response[:1] == '1':
        response = amort.promptUser('Enter %s' % amort.LABEL_LINE_1)
        if response.lower()[:4] == 'quit' or response.lower()[:4] == 'exit':
            break
        amort.Title = response
    elif response[:1] == '2':
        response = amort.promptUser('Enter %s' % amort.LABEL_LINE_2)
        if response.lower()[:4] == 'quit' or response.lower()[:4] == 'exit':
            break
        amort.StartDate = response
    elif response[:1] == '3':
        response = amort.promptUser('Enter %s' % amort.LABEL_LINE_3)
        if response.lower()[:4] == 'quit' or response.lower()[:4] == 'exit':
            break
        amort.Months = response
    elif response[:1] == '4':
        response = amort.promptUser('Enter %s' % amort.LABEL_LINE_4)
        if response.lower()[:4] == 'quit' or response.lower()[:4] == 'exit':
            break
        amort.Amount = response
    elif response[:1] == '5':
        response = amort.promptUser('Enter %s' % amort.LABEL_LINE_5)
        if response.lower()[:4] == 'quit' or response.lower()[:4] == 'exit':
            break
        amort.APR = response
    elif response[:1] == '6':
        response = amort.promptUser('Enter %s' % amort.LABEL_LINE_7)
        if response.lower()[:4] == 'quit' or response.lower()[:4] == 'exit':
            break
        amort.Override = response
