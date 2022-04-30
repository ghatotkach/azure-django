from django.contrib import admin
from .models import (
    Group,
    # Work_Calendar,
    Weekly_Acceptance,
    Diary,
    Student,
    Supervisor,
    Work_Type_And_Period,
    Work_Off_days,
)

# Register your models here.
# admin.site.register(Group)
# admin.site.register(Work_Calendar)
admin.site.register(Weekly_Acceptance)
admin.site.register(Diary)
admin.site.register(Student)
# admin.site.register(Supervisor)
# admin.site.register(Work_Type_And_Period)
admin.site.register(Work_Off_days)

@admin.display(description='Name')
def full_name(obj):
    return (f"{obj.last_name}, {obj.first_name}").title()

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'start_date', 'end_date',)

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = (full_name, 'type',)
    search_fields = ('last_name', 'first_name')

@admin.register(Work_Type_And_Period)
class Work_Type_And_PeriodAdmin(admin.ModelAdmin):
    readonly_fields = ('total_hours',)
    fields = ('start_hour', 'end_hour', 'work_done', 'learning_type', 'diary_id', 'total_hours')
    list_display = ('__str__', 'total_hours', 'learning_type', 'work_done',)
