from django.contrib.auth import get_user_model
from django.test import TestCase

from task.models import (TaskType,
                         Position,
                         Tag,
                         Team,
                         Project,
                         Task)


class ModelsTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")
        self.assertEqual(str(task_type), task_type.name)

    def test_position_str(self):
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), position.name)

    def test_tag_str(self):
        tag = Tag.objects.create(name="test")
        self.assertEqual(str(tag), tag.name)

    def test_create_worker_with_position_and_str(self):
        username = "test"
        password = "test123"
        position = Position.objects.create(name="test1")
        worker = get_user_model().objects.create_user(
            username=username,
            password=password,
            position=position
        )
        self.assertEqual(worker.username, username)
        self.assertEqual(worker.position.name, position.name)
        self.assertEqual(
            str(worker),
            f"{worker.position} - {worker.first_name} {worker.last_name}"
        )
        self.assertTrue(worker.check_password(password))

    def test_team_str(self):
        team = Team.objects.create(name="test")
        self.assertEqual(str(team), team.name)

    def test_project_str(self):
        project = Project.objects.create(
            name="test",
            start_date="2025-09-26"
        )
        self.assertEqual(str(project), project.name)

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test_task_type")
        task = Task.objects.create(
            name="test",
            deadline="2025-09-26",
            is_completed=False,
            task_type=task_type
        )
        self.assertEqual(str(task),
                         f"Task: \"{task.name}\""
                         f"Project: {task.project.name if task.project else 'No project'}"
                         f"Is completed: {task.is_completed}"
                         f"Priority: {task.priority}"
                         f"Deadline: {task.deadline}"
                         f"Description: {task.description}")
