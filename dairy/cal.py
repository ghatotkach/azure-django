import holidays
from datetime import date, timedelta



# class workday:
#     def __init__(self, date, is_work_day):
#         self.date = date
#         self.is_work_day = is_work_day
    
#     def __str__(self):
#         return f"{self.date} {'is work day' if (self.is_work_day) else 'is off day'}"


def set_work_calendar(start_date: date, end_date: date):
    current_date = start_date
    while(current_date <= end_date):
        if current_date.weekday() > 4 or current_date in holidays.Finland():
            # Create database row based on the date and marked as off day
            # print(str(current_date) + " is holiday")
            pass
        else:
            # Create database row based on the date and marked as work day
            # print(str(current_date) + " is work day")
            pass
        current_date += timedelta(days=1)

# holiday_dates = holidays.Finland()
# for holiday in holidays.FIN(years=2022).items():
#     holiday_dates.append(holiday[0])

# class calendar_builder(calendar.Calendar):
#     def __init__(self, year, month) -> None:
#         super().__init__(firstweekday=0)
#         self.year = year
#         self.month = month
    

