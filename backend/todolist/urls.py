from django.urls import path

from todolist.views import *

urlpatterns = [
    path("", view_init.index, name="index"),

    path("api/user/register", view_user.user_register, name="user-register"),
    path("api/user/signin", view_user.user_signin, name="user-signin"),
    path("api/user/signout", view_user.user_signout, name="user-signout"),
    path("api/user/get_username", view_user.get_username, name="get-username"),
    path("api/authentication/status", view_user.authentication_status, name="authentication-status"),

    path("api/project/add", view_task.project_add, name="project-add"),
    path("api/section/add", view_task.section_add, name="section-add"),
    path("api/task/add", view_task.task_add, name="task-add"),
    path("api/todo_item/delete", view_task.todo_item_delete, name="todo-item-delete"),
    path("api/todo_item/update", view_task.todo_item_update, name="todo-item-update"),
    path("api/task_attributes/update", view_task.task_attributes_update, name="task-attributes-update"),
    path("api/todo_item/get_project", view_task.todo_item_get_project, name="todo-item-get-project"),
    path("api/todo_item/get", view_task.todo_item_get, name="todo-item-get"),
    path("api/project/get_by_name", view_task.project_get_by_name, name="project-get-by-name"),
    path("api/section/get_by_name", view_task.section_get_by_name, name="section-get-by-name"),
    path("api/task_attributes/get", view_task.task_attributes_get, name="task-attributes-get"),
    path("api/todo_item/get_list", view_task.todo_item_get_list, name="todo-item-get-list"),
    path("api/todo_item/get_project_list", view_task.todo_item_get_project_list, name="todo-item-get-project-list"),
    path("api/todo_item/get_all", view_task.todo_item_get_all, name="todo-item-get-all"),
    path("api/project/get_all", view_task.project_get_all, name="project-get-all"),
    path("api/task/get_today_list", view_task.task_get_today_list, name="task-get-today-list"),
    path("api/task_attributes/get_list", view_task.task_attributes_get_list, name="task-attributes-get-list"),
    path("api/task/suggest_today", view_task.task_suggest_today, name="task-suggest-today"),
    path("api/task/add_task_today", view_task.task_add_task_today, name="task-add-task-today"),
    path("api/task/remove_from_today", view_task.task_remove_from_today, name="task-remove-from-today"),

    path("api/pomodoro/start", view_pomodoro.pomodoro_start, name="pomodoro-start"),
    path("api/pomodoro/pause", view_pomodoro.pomodoro_pause, name="pomodoro-pause"),
    path("api/pomodoro/continue", view_pomodoro.pomodoro_continue, name="pomodoro-continue"),
    path("api/pomodoro/end", view_pomodoro.pomodoro_end, name="pomodoro-end"),
    path("api/pomodoro/set_task", view_pomodoro.pomodoro_set_task, name="pomodoro-set-task"),
    path("api/pomodoro/set_length", view_pomodoro.pomodoro_set_length, name="pomodoro-set-length"),
    path("api/pomodoro/get_time", view_pomodoro.pomodoro_get_time, name="pomodoro-get-time"),
    path("api/pomodoro/get_history_hour", view_pomodoro.get_history_hour, name="pomodoro-get_history_hour"),
    path("api/pomodoro/get_history_hour_fullday", view_pomodoro.get_history_hour_fullday, name="pomodoro-get-history-hour-fullday"),
    path("api/pomodoro/get_history_day", view_pomodoro.get_history_day, name="pomodoro-get-history-day"),
    path("api/pomodoro/get_last_active_session", view_pomodoro.get_last_active_session, name="pomodoro-get-last-active-session"),

    path("api/website_block/get_block_list", view_website_block.website_block_get_block_list, name="website-block-get-block-list"),
    path("api/website_block/get_urls", view_website_block.website_block_get_urls, name="website-block-get-urls"),
    path("api/website_block/add_url", view_website_block.add_url, name="website-block-add-url"),
    path("api/website_block/delete_url", view_website_block.delete_url, name="website-block-delete-url"),
    path("api/website_block/set_block_status", view_website_block.set_block_status, name="website-block-set-block-status"),

    path("api/test_api", view_test.test_api, name="test-api")
]