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
    
def CanBeLastDayOfMonth(dateEntered):
    canBeLastDayOfMonth = False
    myDate = datetime.datetime.strptime(dateEntered, DATE_FORMAT)
    if myDate.month == 2:
        if myDate.year % 4 == 0:
            canBeLastDayOfMonth = (myDate.day == 29)
        else:
            canBeLastDayOfMonth = (myDate.day == 28)
    elif (myDate.month == 4 
            or myDate.month == 6 
            or myDate.month == 9 
            or myDate.month == 11):
        canBeLastDayOfMonth = (myDate.day == 30)
    else:
        canBeLastDayOfMonth = (myDate.day == 31)
    return canBeLastDayOfMonth

def number_days_in_month(date):
    # start at the 31st, work backwards
    calDay = 31
    while True:
        try:
            date = date.replace(day=calDay)
            return calDay
        except ValueError:
            calDay -= 1
            
def add_months(date_text, numberMonths, use_last_day):
    start_date = datetime.datetime.strptime(date_text, DATE_FORMAT)
    # preserve day
    preserve_day = start_date.day
    # create variable
    date = start_date
    
    # set day to be 1st
    if preserve_day != 1:
        date = date.replace(day=1)
    #loop through months, using first day
    # TODO - optimize this by creating a one-time array
    for z in range(0, numberMonths):    
        # get days of this month
        days_in_this_month = number_days_in_month(date)
        # add days to get desired month
        date += datetime.timedelta(days=days_in_this_month)
    # date is now the first day of the desired month
    if (use_last_day == True):
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
