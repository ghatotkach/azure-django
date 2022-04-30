from django.forms import PasswordInput
from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import date, timedelta
from .models import Group, Work_Off_days, Work_Type_And_Period
from .forms import GroupForm, WorkTypeAndPeriodForm

# Create your views here.


def group_view(request):
    all_groups = Group.objects.all()
    return render(request, "dairy/groups.html", {"all_groups": all_groups})


def create_group(request):
    if request.method == "POST":
        start_date = request.POST.get("startdate")
        end_date = request.POST.get("enddate")
        group_name = request.POST.get("groupname")
        course_name = request.POST.get("coursename")
        new_grp = Group(
            group_name=group_name,
            course_name=course_name,
            start_date=start_date,
            end_date=end_date,
        )
        new_grp.save()

        # Work_Off_days.fill_days(date(start_date), date(end_date), group_name)
    return render(request, "dairy/groupsetupform.html")


# def autoset_holidays(request):
#     start_date = Group.get_start_date()
#     end_date = Group.get_end_date()
#     grp_name = Group.get_group_name()
#     Work_Off_days.fill_days(start_date, end_date, grp_name)

#     return render(request, "dairy/setholidays.html")
def group_form(request):
    submitted = False
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/group/add?submitted=True/")
    else:
        form = GroupForm
        if 'submitted' in request.GET:
            submitted = True
    form = GroupForm
    return render(request, "dairy/group_form.html", {'form': form, 'submitted': submitted})

def work_period_form(request):
    submitted = False
    if request.method == "POST":
        form = WorkTypeAndPeriodForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/work/add?submitted=True/")
    else:
        form = WorkTypeAndPeriodForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, "dairy/work_period_form.html", {'form': form, 'submitted': submitted})

