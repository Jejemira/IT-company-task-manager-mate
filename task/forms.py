from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from task.models import TaskType, Position, Task


class TaskTypeNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255)


class PositionNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255)


class TaskDeadlineSearchForm(forms.Form):
    deadline = forms.DateTimeField()


class TaskForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = "__all__"
