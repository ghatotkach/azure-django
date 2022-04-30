from datetime import date, timedelta, datetime
from tkinter import W

# import calendar
import holidays


def weekly_Calendar():

    total_weeks = number_of_weeks(date(2022, 1, 1), date(2022, 1, 30))
    print(total_weeks)
    setup_OneWeek__calendar(date(2022, 4, 29))


def isHoliday(day: date):
    if day.weekday() > 4 or day in holidays.Finland():
        return False
    else:
        return True


def number_of_weeks(start_date: date, end_date: date):
    if end_date > start_date:
        number_of_days = (end_date - start_date).days
        print(number_of_days)
        return number_of_days // 7


# weekly_Calendar()


def setup_OneWeek__calendar(start_date: date):
    # my_cale = calendar.Calendar(firstweekday=0)
    # ?? Week should start from Monday..number of days in week ma-su
    what_day = start_date.weekday()
    print("week day : ", what_day)
    one_day = timedelta(days=1)
    if what_day == 0:
        end_week_date = start_date + 6 * one_day
    elif what_day == 1:
        end_week_date = start_date + 5 * one_day
    elif what_day == 2:
        end_week_date = start_date + 4 * one_day
    elif what_day == 3:
        end_week_date = start_date + one_day
    elif what_day == 4:
        end_week_date = start_date

    current_date = start_date
    # end_week_date = start_date + 7 * timedelta(days=1)
    is_workday = []
    while current_date <= end_week_date:
        is_workday.append(isHoliday(current_date))
        current_date += timedelta(days=1)
    print(is_workday)


if __name__ == "__main__":
    weekly_Calendar()
