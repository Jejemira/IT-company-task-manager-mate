from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.
class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self) -> str:
        return f"{self.position} - {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse(
            "task:worker-detail",
            kwargs={"pk": self.pk}
        )


class Team(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        Worker,
        related_name="teams"
    )

    def __str__(self) -> str:
        return self.name

    @property
    def members_count(self) -> int:
        return self.members.count()


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    teams = models.ManyToManyField(
        Team,
        related_name="projects"
    )
    manager = models.ForeignKey(
        Worker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="manager_projects"
    )

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        ("URGENT", "Urgent"),
        ("HIGH", "High"),
        ("MEDIUM", "Medium"),
        ("LOW", "Low")
    )

    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks"
    )
    tag = models.ManyToManyField(
        Tag,
        related_name="tasks"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return (f"Task: \"{self.name}\""
                f"Project: {self.project.name if self.project else 'No project'}"
                f"Is completed: {self.is_completed}"
                f"Priority: {self.priority}"
                f"Deadline: {self.deadline}"
                f"Description: {self.description}")
