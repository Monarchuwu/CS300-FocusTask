from django.urls import path

from .views import view_task, view_user

urlpatterns = [
    path("", view_task.index, name="index"),
    path("api/tasks/add", view_task.task_add, name="task-add"),
    path("api/users/register", view_user.user_register, name="user-register"),
]