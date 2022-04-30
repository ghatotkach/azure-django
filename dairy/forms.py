from turtle import width
from django import forms
from .models import Group, Weekly_Acceptance, Work_Type_And_Period

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        # 
        # fields = "__all__"
        fields = ('group_name', 'course_name', 'start_date', 'end_date',)
        widgets = {
            'group_name': forms.TextInput(attrs={}),    # custom 'class': 'group-form', or tailwind css
            'couse_name': forms.TextInput(),            # 'placeholder': 'Course Name', or similar, to add place holder text
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

        # We can edit text labels here
        # labels = {
        #     'group_name': 'This is Group name:', 
        #     'course_name': 'Course name:', 
        #     'start_date': 'Start date:', 
        #     'end_date': 'End date:',
        # }

class WorkTypeAndPeriodForm(forms.ModelForm):
    class Meta:
        model = Work_Type_And_Period
        fields = ('start_hour', 'end_hour', 'work_done', 'learning_type', 'diary_id')
        widgets = {
            'start_hour': forms.TimeInput(attrs={'type': 'time'}),
            'end_hour': forms.TimeInput(attrs={'type': 'time'}),
        }

