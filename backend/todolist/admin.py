from django.contrib import admin
from .models import Task, Archive, TaskContainer
# Register your models here.
admin.site.register(Task)
admin.site.register(TaskContainer)