from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from task.forms import (TaskTypeNameSearchForm,
                        PositionNameSearchForm,
                        TaskDeadlineSearchForm,
                        TaskForm,
                        WorkerUsernameSearchForm,
                        WorkerCreationForm,
                        WorkerPositionUpdateForm,
                        TagNameSearchForm,
                        TeamNameSearchForm,
                        TeamForm,
                        ProjectNameSearchForm,
                        ProjectForm,
                        UserLoginForm)
from task.models import (Worker,
                         Team,
                         Project,
                         Task,
                         TaskType,
                         Position,
                         Tag)


# Create your views here.
@login_required
def index(request):
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()
    num_projects = Project.objects.count()
    num_tasks = Task.objects.count()
    num_task_types = TaskType.objects.count()
    num_positions = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_teams": num_teams,
        "num_workers": num_workers,
        "num_projects": num_projects,
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


class UserLoginView(LoginView):
  template_name = "accounts/sign-in.html"
  form_class = UserLoginForm

def logout_view(request):
  logout(request)
  return redirect("/accounts/login")


class TaskTypeListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task/tasktype_list.html"
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(
            TaskTypeListView,
            self
        ).get_context_data(**kwargs)
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
        context = super(
            PositionListView,
            self
        ).get_context_data(**kwargs)
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


class TagListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Tag
    context_object_name = "tag_list"
    template_name = "task/tag_list.html"
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(
            TagListView,
            self
        ).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TagNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Tag.objects.all()
        form = TagNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TagCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task:tag-list")


class TagUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task:tag-list")


class TagDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Tag
    success_url = reverse_lazy("task:tag-list")


class TeamListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Team
    paginate_by = 5
    queryset = Team.objects.prefetch_related("members")

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(
            TeamListView,
            self
        ).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TeamNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Team.objects.all()
        form = TeamNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TeamDetailView(
    LoginRequiredMixin,
    generic.DetailView
):
    model = Team
    queryset = Team.objects.prefetch_related("members")


class TeamCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task:team-list")


class TeamUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task:team-list")


class TeamDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Team
    success_url = reverse_lazy("task:team-list")


class ProjectListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Project
    paginate_by = 5
    queryset = Project.objects.select_related(
        "manager"
    ).prefetch_related("teams")

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(
            ProjectListView,
            self
        ).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        form = ProjectNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class ProjectDetailView(
    LoginRequiredMixin,
    generic.DetailView
):
    model = Project
    queryset = Project.objects.prefetch_related("teams")


class ProjectCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task:project-list")


class ProjectUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("task:project-list")


class ProjectDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Project
    success_url = reverse_lazy("task:project-list")


class TaskListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Task
    paginate_by = 5
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees")

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(
            TaskListView,
            self
        ).get_context_data(**kwargs)
        deadline = self.request.GET.get("deadline", "")
        context["search_form"] = TaskDeadlineSearchForm(
            initial={"deadline": deadline}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type")
        form = TaskDeadlineSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                deadline__date=form.cleaned_data["deadline"]
            )
        return queryset


class TaskDetailView(
    LoginRequiredMixin,
    generic.DetailView
):
    model = Task
    queryset = Task.objects.prefetch_related(
        "assignees"
    ).prefetch_related("project")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["is_worker"] = self.request.user in self.object.worker.all()
    #     return context


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


class WorkerListView(
    LoginRequiredMixin,
    generic.ListView
):
    model = Worker
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(
            WorkerListView,
            self
        ).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = WorkerUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerDetailView(
    LoginRequiredMixin,
    generic.DetailView
):
    model = Worker
    queryset = Worker.objects.all().select_related(
        "position"
    ).prefetch_related(
        "tasks__task_type"
    )


class WorkerCreateView(
    LoginRequiredMixin,
    generic.CreateView
):
    model = Worker
    form_class = WorkerCreationForm


class WorkerPositionUpdateView(
    LoginRequiredMixin,
    generic.UpdateView
):
    model = Worker
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy("task:worker-list")


class WorkerDeleteView(
    LoginRequiredMixin,
    generic.DeleteView
):
    model = Worker
    success_url = reverse_lazy("task:worker-list")


# @login_required
def toggle_assign_to_task(request, pk):
    worker = Worker.objects.get(id=request.user.id)
    if (
        Task.objects.get(id=pk) in worker.tasks.all()
    ):  # probably could check if task exists
        worker.tasks.remove(pk)
    else:
        worker.tasks.add(pk)
    return HttpResponseRedirect(
        reverse_lazy(
            "task:task-detail",
            args=[pk]
        )
    )

