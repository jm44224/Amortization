class AmortizationMonthPayment:
    def __init__(self):
        # initialize variables
        self._paymentDate = ""
        self._beginBalance = 0.00
        self._payment = 0.00
        self._principal = 0.00
        self._interest = 0.00
        self._endBalance = 0.00

    # get / set Payment Date (or Month Number)
    @property
    def payment_date(self):
        return self._paymentDate

    @payment_date.setter
    def payment_date(self, value):
        self._paymentDate = value

    # get / set Begin Balance
    @property
    def beginning_balance(self):
        return self._beginBalance

    @beginning_balance.setter
    def beginning_balance(self, value):
        self._beginBalance = round(float(value), 2)

    # get / set Payment
    @property
    def payment(self):
        return self._payment

    @payment.setter
    def payment(self, value):
        self._payment = round(float(value), 2)

    # get / set principal
    @property
    def principal(self):
        return self._principal

    @principal.setter
    def principal(self, value):
        self._principal = round(float(value), 2)

    # get / set Interest
    @property
    def interest(self):
        return self._interest

    @interest.setter
    def interest(self, value):
        self._interest = round(float(value), 2)

    # get / set End Balance
    @property
    def ending_balance(self):
        return self._endBalance

    @ending_balance.setter
    def ending_balance(self, value):
        self._endBalance = round(float(value), 2)

