from django.urls import path

from .views import view_task, view_user, view_test

urlpatterns = [
    path("", view_task.index, name="index"),
    path("api/tasks/add", view_task.task_add, name="task-add"),
    path("api/users/register", view_user.user_register, name="user-register"),
    path("api/test_api", view_test.test_api, name="test-api"),
]