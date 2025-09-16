from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.
class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.position} - {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse(
            "task:worker-detail",
            kwargs={"pk": self.pk}
        )


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

    def __str__(self):
        return (f"Task: \"{self.name}\""
                f"Is completed: {self.is_completed}"
                f"Priority: {self.priority}"
                f"Deadline: {self.deadline}"
                f"Description: {self.description}")
