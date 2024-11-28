from django.db import models
from django.utils import timezone

# Create your models here.
class UserDB(models.Model):
    userID = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    passwordHash = models.CharField(max_length=100)
    avatarURL = models.URLField(null = True)
    createdAt = models.DateTimeField("Created date", default = timezone.now)

class WebsiteBlockingDB(models.Model):
    blockID = models.CharField(max_length=100, primary_key=True)
    URL = models.URLField()
    UserID = models.ForeignKey(UserDB, on_delete=models.CASCADE)
    createdAt = models.DateTimeField("Created date", default = timezone.now)
    isBlocking = models.BooleanField(default = True)

class PreferencesDB(models.Model):
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

    userID = models.OneToOneField(UserDB, on_delete=models.CASCADE, primary_key=True)
    language = models.CharField(max_length=20, choices=Language.choices, default=Language.ENGLISH)
    timezone = models.CharField(max_length=10, choices=Timezone.choices, default=Timezone.UTC7)
    notification = models.BooleanField(default = False)
    autoBlock = models.BooleanField(default = False)

class AuthenticationDB(models.Model):
    tokenID = models.CharField(max_length=100, primary_key=True)
    userID = models.ForeignKey(UserDB, on_delete=models.CASCADE)
    tokenValue = models.CharField(max_length=100)
    expiryDate = models.DateTimeField("Expiry date")

class LabelDB(models.Model):
    labelID = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)

class TodoItemDB(models.Model):
    itemID = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    parentID = models.ForeignKey("self", on_delete=models.CASCADE)
    createdDate = models.DateTimeField("Created date", default = timezone.now)
    userID = models.ForeignKey(UserDB, on_delete=models.CASCADE)
    itemType = models.TextChoices("Item Type", "Project Section Task")
    labelID = models.ForeignKey(LabelDB, on_delete=models.CASCADE)

class TaskAttributesDB(models.Model):
    class Priority(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "High"
    class Status(models.TextChoices):
        PENDING = "Pending"
        COMPLETED = "Completed"

    taskID = models.OneToOneField(TodoItemDB, on_delete=models.CASCADE, primary_key=True)
    dueDate = models.DateTimeField("Due date")
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.LOW)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    description = models.CharField(max_length = 500, null = True)
    inTodayDate = models.DateTimeField("In Today date", default = timezone.now)

class MediaDB(models.Model):
    mediaID = models.CharField(max_length=100, primary_key=True)
    fileURL = models.URLField()
    taskID = models.ForeignKey(TodoItemDB, on_delete=models.CASCADE)
    uploadedDate = models.DateTimeField("Uploaded date", default = timezone.now)

class LogsDB(models.Model):
    logID = models.CharField(max_length=100, primary_key=True)
    taskID = models.ForeignKey(TodoItemDB, on_delete=models.CASCADE)
    userID = models.ForeignKey(UserDB, on_delete=models.CASCADE)
    logContent = models.CharField(max_length = 500)
    createdAt = models.DateTimeField("Created date", default = timezone.now)
    
class ReminderDB(models.Model):
    reminderID = models.CharField(max_length=100, primary_key=True)
    taskID = models.ForeignKey(TodoItemDB, on_delete=models.CASCADE)
    reminderMode = models.TextChoices("Reminder Mode", "BeforeDueDate AtSpecificMoment")
    timeOffset = models.DurationField()
    specificTime = models.DateTimeField("Specific time")

class PomodoroHistoryDB(models.Model):
    pomodoroID = models.CharField(max_length=100, primary_key=True)
    taskID = models.ForeignKey(TodoItemDB, on_delete=models.CASCADE)
    startTime = models.DateTimeField("Start time")
    duration = models.DurationField()
    endTime = models.DateTimeField("End time")
    status = models.TextChoices("Status", "Completed Canceled")
    createdAt = models.DateTimeField("Created date", default = timezone.now)