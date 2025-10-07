from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task.models import (TaskType,
                         Position,
                         Tag,
                         Team,
                         Project,
                         Task)

TASK_TYPE_URL = reverse("task:task-type-list")


class PublicTaskTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=Position.objects.create(name="test")
        )
        self.client.force_login(self.user)

    def test_retrieve_task_type(self):
        TaskType.objects.create(name="bag")
        TaskType.objects.create(name="QA")
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        task_type = TaskType.objects.all()
        self.assertEqual(
            list(response.context["task_type_list"]),
            list(task_type)
        )
        self.assertTemplateUsed(
            response,
            "task/tasktype_list.html"
        )


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            position=Position.objects.create(name="test")
        )
        self.client.force_login(self.user)

    def test_create_worker(self):
        position = Position.objects.create(name="test")
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "position": position.id,
        }
        self.client.post(
            reverse("task:worker-create"),
            data=form_data
        )
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.position.id, form_data["position"])
