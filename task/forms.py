from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       UsernameField)
from django.core.exceptions import ValidationError

from task.models import Task, Worker, Team, Project


class UserLoginForm(AuthenticationForm):
  username = UsernameField(
      widget=forms.TextInput(
          attrs={
              "class": "form-control form-control-lg",
              "placeholder": "Username"
          }
      )
  )
  password = forms.CharField(
      label=("Password"),
      strip=False,
      widget=forms.PasswordInput(
          attrs={
              "class": "form-control form-control-lg",
              "placeholder": "Password"
          }
      ),
  )


class TaskTypeNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255)


class PositionNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255)


class TagNameSearchForm(forms.Form):
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


class TeamNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255)


class TeamForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = "__all__"


class ProjectNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255)


class ProjectForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
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
        fields = [
            "first_name",
            "last_name",
            "position",
            "username"
        ]

    # def clean_position(self):
    #     return self.cleaned_data["position"]
