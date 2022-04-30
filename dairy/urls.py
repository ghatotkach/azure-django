from django.urls import path
from .views import group_view, create_group, group_form, work_period_form  # ,autoset_holidays

urlpatterns = [
    path("group/", group_view, name="view_groups"),
    path("add-group/", create_group, name="create_group"),
    # path("holiday-setup", autoset_holidays, name="holiday_setup"),
    path("group/add/", group_form, name="add-group"),
    path("work/add/", work_period_form, name="add-work-period"),
]
