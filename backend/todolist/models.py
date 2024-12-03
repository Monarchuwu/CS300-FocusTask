from pyexpat import model
from re import M
import re
from django.db import models
from django.utils import timezone

# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=100)
class RepeatedMode(models.Model):
    name = models.CharField(max_length = 10)
    dayType = models.TextChoices("Day of Week", "Sunday Monday Tuesday Wednesday Thursday Friday Saturday")
    startDuration = models.DateField("Start of Repeat")
    endDuration = models.DateField("End of Repeat")


class Task(models.Model):
    taskID = models.CharField(max_length=100, primary_key=True)
    taskName = models.CharField(max_length=200)
    dueDate = models.DateTimeField("Due date")
    reminder = models.DateTimeField("Reminding date", null = True)
    description = models.CharField(max_length = 500, null = True)
    isDoneState = models.BooleanField(default = False)
    priority = models.TextChoices("Priority", "Red Yellow Green")
    createdDate = models.DateTimeField("Created date", default = timezone.now)
    labels = models.ManyToManyField(Label)
    repeatModeList = models.ManyToManyField(RepeatedMode)



class FileAttachment(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    attachFile = models.FileField()


class URLAttachment(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    attachFile = models.URLField()


class TaskContainer(models.Model):
    createdDate = models.DateTimeField("Created date", default=timezone.now)
    containerName = models.CharField(max_length=100)
    tasksList = models.ManyToManyField(Task)

class Archive(models.Model):
    containerList = models.ManyToManyField(TaskContainer)


class TaskSubrelation(models.Model):
    mainTask = models.ForeignKey(
        Task, related_name="Main_task", on_delete=models.CASCADE)
    subTask = models.ForeignKey(
        Task, related_name="Sub_task",  on_delete=models.CASCADE)

