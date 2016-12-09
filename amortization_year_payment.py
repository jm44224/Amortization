class Amort_YearPayment:
    def __init__ (self):
        # initialize variables
        self._year = ""
        self.__totalPayments = 0.00
        self.__totalInterest = 0.00
        self.__totalPrincipal = 0.00
        self._month01 = None
        self._month02 = None
        self._month03 = None
        self._month04 = None
        self._month05 = None
        self._month06 = None
        self._month07 = None
        self._month08 = None
        self._month09 = None
        self._month10 = None
        self._month11 = None
        self._month12 = None

	# get / set Year
    @property
    def Year(self):
        return self._year
    @Year.setter
    def Year(self, value):
        self._year = value

	# get / set Month01
    @property
    def Month01(self):
        return self._year
    @Year.setter
    def Month01(self, value):
		if isinstance(value, Amort_MonthPayment)
        self._month01 = value
		