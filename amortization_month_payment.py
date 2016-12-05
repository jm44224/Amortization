class Amort_MonthPayment:
    def __init__ (self):
        # initialize variables
        self._paymentDate = ""
        self._beginBalance = 0.00
        self._payment = 0.00
        self._principal = 0.00
        self._interest = 0.00
        self._endBalance = 0.00

    # get / set Payment Date (or Month Number)
    @property
    def PaymentDate(self):
        return self._paymentDate
    @PaymentDate.setter
    def PaymentDate(self, value):
        self._paymentDate = value

    # get / set Begin Balance
    @property
    def BeginBalance(self):
        return self._beginBalance
    @BeginBalance.setter
    def BeginBalance(self, value):
        self._beginBalance = round(float(value), 2)

    # get / set Payment
    @property
    def Payment(self):
        return self._payment
    @Payment.setter
    def Payment(self, value):
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
    def Interest(self):
        return self._interest
    @Interest.setter
    def Interest(self, value):
        self._interest = round(float(value), 2)

    # get / set End Balance
    @property
    def EndBalance(self):
        return self._endBalance
    @EndBalance.setter
    def EndBalance(self, value):
        self._endBalance = round(float(value), 2)

