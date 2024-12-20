from django.urls import path

from todolist.views import *

urlpatterns = [
    path("", view_init.index, name="index"),

    path("api/user/register", view_user.user_register, name="user-register"),
    path("api/user/signin", view_user.user_signin, name="user-signin"),
    path("api/user/signout", view_user.user_signout, name="user-signout"),
    path("api/authentication/status", view_user.authentication_status, name="authentication-status"),

    path("api/project/add", view_task.project_add, name="project-add"),
    path("api/section/add", view_task.section_add, name="section-add"),
    path("api/task/add", view_task.task_add, name="task-add"),
    path("api/todo_item/delete", view_task.todo_item_delete, name="todo-item-delete"),
    path("api/todo_item/update", view_task.todo_item_update, name="todo-item-update"),
    path("api/task_attributes/update", view_task.task_attributes_update, name="task-attributes-update"),
    path("api/todo_item/get_project", view_task.todo_item_get_project, name="todo-item-get-project"),
    path("api/todo_item/get", view_task.todo_item_get, name="todo-item-get"),
    path("api/task_attributes/get", view_task.task_attributes_get, name="task-attributes-get"),
    path("api/todo_item/get_list", view_task.todo_item_get_list, name="todo-item-get-list"),
    path("api/todo_item/get_all", view_task.todo_item_get_all, name="todo-item-get-all"),
    path("api/task/get_today_list", view_task.task_get_today_list, name="task-get-today-list"),
    path("api/task_attributes/get_list", view_task.task_attributes_get_list, name="task-attributes-get-list"),

    path("api/test_api", view_test.test_api, name="test-api")
]