from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task.forms import (TaskTypeNameSearchForm,
                        PositionNameSearchForm,
                        TaskDeadlineSearchForm,
                        TaskForm,)
from task.models import (Worker,
                         Task,
                         TaskType,
                         Position)


# Create your views here.
@login_required
def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_workers": num_workers,
        "num_tasks": num_tasks,
        "num_task_types": num_task_types,
        "num_positions": num_positions,
        "num_visits": num_visits + 1,
    }

    return render(
        request,
        "task/index.html",
        context=context
    )


class TaskTypeListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task/task_type_list.html"
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TaskTypeCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = TaskType
    success_url = reverse_lazy("task:task-type-list")


class PositionListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Position
    context_object_name = "position_list"
    template_name = "task/position_list.html"
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class PositionCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Position
    success_url = reverse_lazy("task:position-list")


class TaskListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Task
    paginate_by = 5
    queryset = Task.objects.select_related("priority")

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(TaskListView, self).get_context_data(**kwargs)
        deadline = self.request.GET.get("deadline", "")
        context["search_form"] = TaskDeadlineSearchForm(
            initial={"deadline": deadline}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("deadline")
        form = TaskDeadlineSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                model__icontains=form.cleaned_data["deadline"]
            )
        return queryset


class TaskDetailView(
    LoginRequiredMixin,
    generic.DetailView
):
    model = Task


class TaskCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task:task-list")


class TaskDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Task
    success_url = reverse_lazy("task:task-list")


@login_required
def toggle_assign_to_task(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if (
        Task.objects.get(id=pk) in worker.tasks.all()
    ):  # probably could check if car exists
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(
        reverse_lazy(
            "task:task-detail",
            args=[pk]
        )
    )

