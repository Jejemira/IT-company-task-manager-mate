from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def __str__(self):
        return f"{self.position} - {self.first_name} {self.last_name}"


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "URGENT"
        HIGH = "HIGH"
        MEDIUM = "MEDIUM"
        LOW = "LOW"

        PRIORITY_CHOICES = [
            (URGENT, "Urgent"),
            (HIGH, "High"),
            (MEDIUM, "Medium"),
            (LOW, "Low")
        ]


    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.PRIORITY_CHOICES,
        default=Priority.MEDIUM
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
