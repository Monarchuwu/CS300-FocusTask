from re import M
import re
from django.db import models
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    taskID = models.CharField(max_length=100, primary_key=True)
    taskName = models.CharField(max_length=200)
    dueDate = models.DateTimeField("Due date")
    reminder = models.DateTimeField("Reminding date", null=True)
    repeatOne = models.BooleanField(default=False)
    repeatEveryDay = models.BooleanField(default=False)
    repeatEveryWeek = models.BooleanField(default=False)
    description = models.CharField(max_length=500, null=True)
    isDoneState = models.BooleanField(default=False)
    createdDate = models.DateTimeField("Created date", default=timezone.now)
    # label = models.Many


class Label(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class FileAttachment(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    attachFile = models.FileField()


class URLAttachment(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    attachFile = models.URLField()


class TaskContainer(models.Model):
    createdDate = models.DateTimeField("Created date", default=timezone.now)
    containerName = models.CharField(max_length=100)


class TaskRelation(models.Model):
    taskContainer = models.ForeignKey(TaskContainer, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskSubrelation(models.Model):
    mainTask = models.ForeignKey(
        Task, related_name="Main_task", on_delete=models.CASCADE)
    subTask = models.ForeignKey(
        Task, related_name="Sub_task",  on_delete=models.CASCADE)
