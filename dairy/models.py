from email.headerregistry import Group
from pyexpat import model
from xmlrpc.client import Boolean
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import holidays
from datetime import date, datetime, timedelta
from django.db.models.signals import post_save


class Work_Off_days(models.Model):
    isHoliday = models.BooleanField(default=False)
    day = models.DateField()
    group_name = models.ForeignKey("Group", on_delete=models.CASCADE)

    # we could call this to add more dates, by starting from 
    # next day after previous end date
    def fill_days(sender, instance, created, **kwargs):
        if created:
            instance_obj = Group.objects.get( pk=instance.pk)
            current_date = getattr(instance_obj, 'start_date')
            while current_date <= getattr(instance_obj, 'end_date'):
                if current_date.weekday() > 4 or current_date in holidays.Finland():
                    obj = Work_Off_days.objects.create(
                        isHoliday=False, day=current_date, group_name=instance
                    )
                    obj.save()
                else:
                    obj = Work_Off_days.objects.create(
                        isHoliday=True, day=current_date, group_name=instance
                    )
                    obj.save()
                current_date += timedelta(days=1)

    class Meta:
        verbose_name = "Work days and Holiday"

    def __str__(self):
        return f"{self.day} is {'work day'if self.isHoliday else 'holiday'}"


post_save.connect(Work_Off_days.fill_days, sender="dairy.Group")


# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=70)
    course_name = models.CharField(max_length=70)
    # Start and end of course
    start_date = models.DateField()
    end_date = models.DateField()

    # Meta Class for visible names in admin panel
    class Meta:
        verbose_name = "Course Group"

    # @staticmethod
    # def get_start_date():
    #     return Group.start_date

    # @staticmethod
    # def get_end_date():
    #     return Group.end_date

    # @staticmethod
    # def get_group_name():
    #     return Group.group_name

    def __str__(self):
        return self.group_name


class Supervisor(models.Model):
    class SupervisorType(models.TextChoices):
        TEACHER = "t", _("Teacher")
        SUPERVISOR = "s", _("Supervisor")

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField()
    type = models.CharField(
        max_length=1,
        choices=SupervisorType.choices,
        default=SupervisorType.TEACHER,
    )

    # Meta Class for visible names in admin panel
    class Meta:
        verbose_name = "Supervisor"

    def __str__(self):
        return f"{self.type} - {self.last_name}, {self.first_name}"


class Weekly_Acceptance(models.Model):
    class Estimation(models.TextChoices):
        NOT = "0", _("Not at all")
        SOME = "1", _("Somewhat")
        ENOUGH = "2", _("Appropriate amount")

    evaluation_week = models.PositiveIntegerField()
    wasSupported = models.CharField(
        max_length=1,
        choices=Estimation.choices,
    )
    wasProvidedDevSupport = models.CharField(
        max_length=1,
        choices=Estimation.choices,
    )
    didLearn = models.CharField(
        max_length=1,
        choices=Estimation.choices,
    )
    # Added from Acceptance to from Weekly_Acceptance
    supervisor_id = models.ForeignKey(Supervisor, on_delete=models.RESTRICT)
    student_id = models.ForeignKey("Student", on_delete=models.CASCADE)
    accepted_date = models.DateField(null=True, blank=True)
    accepted_date_student = models.DateField(null=True, blank=True)
    student_id = models.ForeignKey("Student", on_delete=models.CASCADE)
    # Meta Class for visible names in admin panel

    class Meta:
        verbose_name = "Student & Supervisor Acceptance"

    def __str__(self):
        return f"{self.evaluation_week}"


class Diary(models.Model):

    diary_date = models.DateField()
    student_id = models.ForeignKey("Student", on_delete=models.CASCADE)
    is_work_day = models.BooleanField()

    class Meta:
        verbose_name = "Diaries"

    def __str__(self):
        return f"{self.diary_date}: {self.student_id}"


class Work_Type_And_Period(models.Model):
    class LearningType(models.TextChoices):
        REMOTE = "WR", _("Working remote")
        ONSITE = "OS", _("On the site")
        HYBRID = "HM", _("Hybrid model")

    start_hour = models.TimeField()
    end_hour = models.TimeField()
    work_done = models.TextField()  # As I understood doesn't work with Oracle
    learning_type = models.CharField(
        max_length=2,
        choices=LearningType.choices,
    )
    diary_id = models.ForeignKey(Diary, on_delete=models.CASCADE)

    total_hours = models.FloatField()  # Set the calculation

    @property
    def total_hours(self):
        """Returns datetime object with duration between start_hour and end_hour."""
        if (not self.start_hour or not self.end_hour):
            return 0
        today = date.today()
        return (datetime.combine(today, self.end_hour) - datetime.combine(today, self.start_hour))

    class Meta:
        verbose_name = "Diary content & hour"

    def __str__(self):
        return f"{self.diary_id}: {self.start_hour}-{self.end_hour}"




class Student(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField()
    group_id = models.ForeignKey(
        Group, on_delete=models.CASCADE
    )  # Students deleted when group removed
    supervisor_id = models.ForeignKey(
        Supervisor, null=True, on_delete=models.SET_NULL
    )  # If supervisor leaves, student is not kicked out of the school
    # diary_id = models.ForeignKey(Diary, on_delete=models.RESTRICT)
    class Meta:
        verbose_name = "Student"

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"


# class Weekly_Calendar(models.Model):
#     is_workday = models.BooleanField(default=True)
#     group_id = models.ForeignKey("Group", on_delete=models.CASCADE)

#     def save(self, *args, **kwargs):
#         self.is_workdday = self.set_work_calendar(
#             # do some work to set workdays by calling method
#         )

#     @classmethod
#     def isHoliday(self, day: date):
#         if day.weekday() > 4 or day in holidays.Finland():
#             return False
#         else:
#             return True

#     def number_of_weeks(self, start_date: date, end_date: date):
#         number_of_days = abs(start_date - end_date).days
#         return number_of_days // 7
