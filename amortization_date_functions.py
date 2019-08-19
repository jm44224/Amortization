import datetime

"""

Code to add one month to a given date in Python.
Parameter to optionally select the last day of the month.

"""
DATE_FORMAT = '%Y-%m-%d'


# validates that a given date is in the correct format
# validates that a given date is actually a date
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, DATE_FORMAT)
        return True
    except ValueError:
        raise


"""
https://support.microsoft.com/en-us/kb/214019
To determine whether a year is a leap year, follow these steps:
1 If the year is evenly divisible by 4, go to step 2. Otherwise, go to step 5.
2 If the year is evenly divisible by 100, go to step 3. Otherwise, go to step 4.
3 If the year is evenly divisible by 400, go to step 4. Otherwise, go to step 5.
4 The year is a leap year (it has 366 days).
5 The year is not a leap year (it has 365 days).
"""


def is_leap_year(year):
    # If the year is NOT evenly divisible by 4, it is NOT a leap year
    if year % 4 != 0:
        return False
    # If the year is NOT evenly divisible by 100, it IS a leap year
    if year % 100 != 0:
        return True
    # If the year is evenly divisible by 400, it IS a leap year
    if year % 400 == 0:
        return True
    # else, it is NOT a leap year
    return False


def can_be_last_day_of_month(date_entered):
    date_without_time = datetime.datetime.strptime(date_entered, DATE_FORMAT)
    if date_without_time.month == 2:
        if is_leap_year(date_without_time.year):
            return_value = (date_without_time.day == 29)
        else:
            return_value = (date_without_time.day == 28)
    elif (date_without_time.month == 4
            or date_without_time.month == 6
            or date_without_time.month == 9
            or date_without_time.month == 11):
        return_value = (date_without_time.day == 30)
    else:
        return_value = (date_without_time.day == 31)
    return return_value


def number_days_in_month(date):
    # start at the 31st, work backwards
    return_value = 31
    while True:
        try:
            date = date.replace(day=return_value)
            return return_value
        except ValueError:
            return_value -= 1


def add_months(date_text, number_months, use_last_day):
    start_date = datetime.datetime.strptime(date_text, DATE_FORMAT)
    # preserve day
    preserve_day = start_date.day
    # create variable
    date = start_date
    
    # set day to be 1st
    if preserve_day != 1:
        date = date.replace(day=1)
    # loop through months, using first day
    # TODO - optimize this by creating a one-time array
    for z in range(0, number_months):
        # get days of this month
        days_in_this_month = number_days_in_month(date)
        # add days to get desired month
        date += datetime.timedelta(days=days_in_this_month)
    # date is now the first day of the desired month
    if use_last_day:
        days_in_this_month = number_days_in_month(date)
        date = date.replace(day=days_in_this_month)
        return date.strftime(DATE_FORMAT)
    else:
        # set preferred day, subtract back until valid
        while True:
            try:
                date = date.replace(day=preserve_day)
                return date.strftime(DATE_FORMAT)
            except ValueError:
                preserve_day -= 1    
