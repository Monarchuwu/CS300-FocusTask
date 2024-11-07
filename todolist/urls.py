from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('toggle-task-done/<str:task_id>/', views.toggle_task_done, name='toggle_task_done'),
    path('add-task/', views.add_task, name='add_task'),
]