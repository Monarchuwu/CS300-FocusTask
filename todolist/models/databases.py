from django.db import models
from django.utils import timezone
from datetime import datetime
from . import objects

# Create your models here.
class MyDB(models.Model):
    def get_data_object(self):
        return NotImplementedError("This method should be implemented in the derived class")

class UserDB(MyDB):
    userID = models.IntegerField(primary_key = True)
    username = models.CharField(max_length = 100)
    email = models.EmailField()
    passwordHash = models.CharField(max_length = 100)
    avatarURL = models.URLField(null = True, blank = True)
    createdAt = models.DateTimeField("Created date", default = timezone.now)

    def get_data_object(self):
        return objects.User(
            self.userID,
            self.username,
            self.email,
            self.passwordHash,
            self.avatarURL,
            self.createdAt
        )

class WebsiteBlockingDB(MyDB):
    blockID = models.IntegerField(primary_key = True)
    URL = models.URLField()
    UserID = models.ForeignKey(UserDB, on_delete = models.CASCADE)
    createdAt = models.DateTimeField("Created date", default = timezone.now)
    isBlocking = models.BooleanField(default = True)

    def get_data_object(self):
        return objects.WebsiteBlocking(
            self.blockID,
            self.URL,
            self.UserID.userID,
            self.createdAt,
            self.isBlocking
        )

class PreferencesDB(MyDB):
    class Language(models.TextChoices):
        ENGLISH = "English"
        VIETNAMESE = "Vietnamese"
    class Timezone(models.TextChoices):
        UTC0 = "UTC+0"
        UTC1 = "UTC+1"
        UTC2 = "UTC+2"
        UTC3 = "UTC+3"
        UTC4 = "UTC+4"
        UTC5 = "UTC+5"
        UTC6 = "UTC+6"
        UTC7 = "UTC+7"
        UTC8 = "UTC+8"
        UTC9 = "UTC+9"
        UTC10 = "UTC+10"
        UTC11 = "UTC+11"
        UTC12 = "UTC+12"
        UTC_1 = "UTC-1"
        UTC_2 = "UTC-2"
        UTC_3 = "UTC-3"
        UTC_4 = "UTC-4"
        UTC_5 = "UTC-5"
        UTC_6 = "UTC-6"
        UTC_7 = "UTC-7"
        UTC_8 = "UTC-8"
        UTC_9 = "UTC-9"
        UTC_10 = "UTC-10"
        UTC_11 = "UTC-11"
        UTC_12 = "UTC-12"

    userID = models.OneToOneField(UserDB, on_delete = models.CASCADE, primary_key = True)
    language = models.CharField(max_length = 20, choices = Language.choices, default = Language.ENGLISH)
    timezone = models.CharField(max_length = 10, choices = Timezone.choices, default = Timezone.UTC7)
    notification = models.BooleanField(default = False)
    autoBlock = models.BooleanField(default = False)

    def get_data_object(self):
        return objects.Preferences(
            self.userID.userID,
            self.language,
            self.timezone,
            self.notification,
            self.autoBlock
        )

class AuthenticationTokenDB(MyDB):
    tokenID = models.IntegerField(primary_key = True)
    userID = models.ForeignKey(UserDB, on_delete = models.CASCADE)
    tokenValue = models.CharField(max_length = 100)
    expiryDate = models.DateTimeField("Expiry date")

    def get_data_object(self):
        return objects.AuthenticationToken(
            self.tokenID,
            self.userID.userID,
            self.tokenValue,
            self.expiryDate
        )

class LabelDB(MyDB):
    labelID = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)

    def get_data_object(self):
        return objects.Label(
            self.labelID,
            self.name
        )

class TodoItemDB(MyDB):
    class ItemType(models.TextChoices):
        PROJECT = "Project"
        SECTION = "Section"
        TASK = "Task"

    itemID = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    parentID = models.ForeignKey("self", on_delete = models.CASCADE, null = True, blank = True)
    createdDate = models.DateTimeField("Created date", default = timezone.now)
    userID = models.ForeignKey(UserDB, on_delete = models.CASCADE)
    itemType = models.CharField(max_length = 10, choices=ItemType.choices, default = ItemType.TASK)
    labelID = models.ForeignKey(LabelDB, on_delete = models.CASCADE, null = True, blank = True)

    def get_data_object(self):
        return objects.TodoItem(
            self.itemID,
            self.name,
            self.parentID.itemID if self.parentID else None,
            self.createdDate,
            self.userID.userID,
            self.itemType,
            self.labelID.labelID if self.labelID else None
        )

class TaskAttributesDB(MyDB):
    class Priority(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "High"
    class Status(models.TextChoices):
        PENDING = "Pending"
        COMPLETED = "Completed"

    taskID = models.OneToOneField(TodoItemDB, on_delete = models.CASCADE, primary_key = True)
    dueDate = models.DateTimeField("Due date", null = True, blank = True)
    priority = models.CharField(max_length = 10, choices = Priority.choices, default = Priority.LOW)
    status = models.CharField(max_length = 10, choices = Status.choices, default = Status.PENDING)
    description = models.CharField(max_length = 500, default = "")
    inTodayDate = models.DateTimeField("In Today date", default = datetime(2100, 1, 1))

    def get_data_object(self):
        return objects.TaskAttributes(
            self.taskID.itemID,
            self.dueDate,
            self.priority,
            self.status,
            self.description,
            self.inTodayDate
        )

class MediaDB(MyDB):
    mediaID = models.IntegerField(primary_key = True)
    fileURL = models.URLField()
    taskID = models.ForeignKey(TodoItemDB, on_delete = models.CASCADE)
    uploadedDate = models.DateTimeField("Uploaded date", default = timezone.now)

    def get_data_object(self):
        return objects.Media(
            self.mediaID,
            self.fileURL,
            self.taskID.itemID,
            self.uploadedDate
        )

class LogsDB(MyDB):
    logID = models.IntegerField(primary_key = True)
    taskID = models.ForeignKey(TodoItemDB, on_delete = models.CASCADE)
    logContent = models.CharField(max_length = 500)
    createdAt = models.DateTimeField("Created date", default = timezone.now)

    def get_data_object(self):
        return objects.Logs(
            self.logID,
            self.taskID.itemID,
            self.logContent,
            self.createdAt
        )
    
class ReminderDB(MyDB):
    class ReminderMode(models.TextChoices):
        BEFORE_DUE_DATE = "Before Due Date"
        AT_SPECIFIC_MOMENT = "At Specific Moment"

    reminderID = models.IntegerField(primary_key = True)
    taskID = models.ForeignKey(TodoItemDB, on_delete = models.CASCADE)
    reminderMode = models.CharField(max_length = 20, choices = ReminderMode.choices, default = ReminderMode.BEFORE_DUE_DATE)
    timeOffset = models.DurationField()
    specificTime = models.DateTimeField("Specific time", null = True, blank = True)

    def get_data_object(self):
        return objects.Reminder(
            self.reminderID,
            self.taskID.itemID,
            self.reminderMode,
            self.timeOffset,
            self.specificTime
        )

class PomodoroHistoryDB(MyDB):
    class Status(models.TextChoices):
        COMPLETED = "Completed"
        RUNNING = "Running"
        PAUSED = "Paused"
        CANCELED = "Canceled"

    pomodoroID = models.IntegerField(primary_key = True)
    taskID = models.ForeignKey(TodoItemDB, on_delete = models.CASCADE)
    startTime = models.DateTimeField("Start time")
    duration = models.DurationField()
    currentDuration = models.DurationField(null=True)
    endTime = models.DateTimeField("End time")
    status = models.CharField(max_length = 10, choices = Status.choices, default = Status.COMPLETED)
    createdAt = models.DateTimeField("Created date", default = timezone.now)

    def get_data_object(self):
        return objects.PomodoroHistory(
            self.pomodoroID,
            self.taskID.itemID,
            self.startTime,
            self.duration,
            self.endTime,
            self.status,
            self.createdAt
        )