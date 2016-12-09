import datetime
import amortization_date_functions

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
        try:
            if float(value) >=0.01:
                self._loanAmount  = round(float(value), 2)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Annual Percentage Rate, validate as a positive percentage         
    @property
    def APR(self):
        return self._percent
    @APR.setter
    def APR(self, value):
        try:
            if float(value) >=0.0 and float(value) <= 100.0:
                value = round(float(value), 4)
                self._percent = float(value)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Months of Loan, validate as a positive integer          
    @property
    def Months(self):
        return self._loanMonths
    @Months.setter
    def Months(self, value):
        try:
            if int(value) >=1:
                self._loanMonths = int(value)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Monthly Payment Override, validate as a positive number
    @property
    def Override(self):
        return self._overridePayment
    @Override.setter
    def Override(self, value):
        try:
            if float(value) >=0.01:
                self._overridePayment  = round(float(value), 2)
            else:
                raise ValueError
        except ValueError:
            raise ValueError

    # get / set Start Date of Payment, validate as a valid date format
    # this is not yet used            
    @property
    def StartDate(self):
        return self._startDate
    @StartDate.setter
    def StartDate(self, value):
        try:
            if amortization_date_functions.ValidateDate(value) == True:
                self._startDate = value
        except ValueError:
            raise 
        
    # get / set Loan Title
    # this is not yet used    
    @property
    def Title(self):
        return self._title
    @Title.setter
    def Title(self, value):
        self._title = str(value)

