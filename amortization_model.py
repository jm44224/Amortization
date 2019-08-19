import datetime
from amortization_date_functions import validate_date


class AmortizationModel:
    def __init__(self):
        # initialize variables
        self._title = ""
        self._startDate = str(datetime.date.today())
        self._loanMonths = 0
        self._loanAmount = 0.00
        self._percent = 0.0000
        self._calcPayment = 0.00
        self._overridePayment = 0.00
    
    # get / set Loan Amount, validate as a positive number
    @property
    def loan_amount(self):
        return self._loanAmount

    @loan_amount.setter
    def loan_amount(self, value):
        try:
            if float(value) >= 0.01:
                self._loanAmount = round(float(value), 2)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Annual Percentage Rate, validate as a positive percentage         
    @property
    def annual_percentage_rate(self):
        return self._percent

    @annual_percentage_rate.setter
    def annual_percentage_rate(self, value):
        try:
            if 0.0 <= float(value) <= 100.0:
                value = round(float(value), 4)
                self._percent = float(value)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Months of Loan, validate as a positive integer          
    @property
    def loan_months(self):
        return self._loanMonths

    @loan_months.setter
    def loan_months(self, value):
        try:
            if int(value) >= 1:
                self._loanMonths = int(value)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Monthly Payment Override, validate as a positive number
    @property
    def override_payment(self):
        return self._overridePayment

    @override_payment.setter
    def override_payment(self, value):
        try:
            if float(value) >= 0.01:
                self._overridePayment = round(float(value), 2)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Calculated Payment, validate as a positive number
    @property
    def calculated_payment(self):
        return self._calcPayment

    @calculated_payment.setter
    def calculated_payment(self, value):
        try:
            if float(value) >= 0.00:
                self._calcPayment = round(float(value), 2)
            else:
                raise ValueError
        except ValueError:
            raise ValueError
        
    # get / set Start Date of Payment, validate as a valid date format
    # this is not yet used            
    @property
    def start_date(self):
        return self._startDate

    @start_date.setter
    def start_date(self, value):
        try:
            if validate_date(value):
                self._startDate = value
        except ValueError:
            raise 
        
    # get / set Loan Title
    # this is not yet used    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = str(value)

