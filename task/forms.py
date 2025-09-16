from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from task.models import Task, Worker


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


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(max_length=255)


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )

    # def clean_position(self):
    #     return self.cleaned_data["position"]


class WorkerPositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["position"]

    # def clean_position(self):
    #     return self.cleaned_data["position"]
