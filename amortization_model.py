
import datetime

class Amort_Model:
    def __init__ (self):
        # initialize variables
        self._title = ""
        self._startDate = datetime.date.today()
        self._loanMonths = 0
        self._loanAmount = 0.00
        self._percent = 0.0000
        self._calcPayment = 0.00
        self._overridePayment = 0.00

	# get / set Loan Amount, validate as a positive number
    @property
    def Amount(self):
        return self._loanAmount
    @Amount.setter
    def Amount(self, value):
        if float(value) >=0.01:
            self._loanAmount  = round(float(value), 2)
        else:
            print(str(value) + " is not a valid number for amount (minimum of 0.01).")

    # get / set Annual Percentage Rate, validate as a positive percentage         
    @property
    def APR(self):
        return self._percent
    @APR.setter
    def APR(self, value):
        if float(value) >=0.0 and float(value) <=100.0:
            value = round(float(value), 4)
            self._percent = float(value)
        else:
            print(str(value) + " is not a valid number for percentage (0.0000 to 100.0000).")

    # get / set Months of Loan, validate as a positive integer          
    @property
    def Months(self):
        return self._loanMonths
    @Months.setter
    def Months(self, value):
        if int(value) >=1:
            self._loanMonths = int(value)
        else:
            print(str(value) + " is not a valid number for months (minimum of 1).")

    # get / set Monthly Payment Override, validate as a positive number
    @property
    def Override(self):
        return self._overridePayment
    @Override.setter
    def Override(self, value):
        if float(value) >=0.01:
            self._overridePayment  = round(float(value), 2)
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

