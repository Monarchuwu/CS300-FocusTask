from datetime import datetime, timedelta

class User:
    def __init__(self,
                 userID: int,
                 username: str,
                 email: str,
                 passwordHash: str,
                 avatarURL: str | None,
                 createdAt: datetime):
        self.userID = userID
        self.username = username
        self.email = email
        self.passwordHash = passwordHash
        self.avatarURL = avatarURL
        self.createdAt = createdAt

class WebsiteBlocking:
    def __init__(self,
                 blockID: int,
                 URL: str,
                 UserID: int,
                 createdAt: datetime,
                 isBlocking: bool):
        self.blockID = blockID
        self.URL = URL
        self.UserID = UserID
        self.createdAt = createdAt
        self.isBlocking = isBlocking

class Preferences:
    def __init__(self,
                 userID: int,
                 language: str,
                 timezone: str,
                 notification: bool,
                 autoBlock: bool):
        self.userID = userID
        self.language = language
        self.timezone = timezone
        self.notification = notification
        self.autoBlock = autoBlock

class AuthenticationToken:
    def __init__(self,
                 tokenID: int,
                 userID: int,
                 tokenValue: str,
                 expiryDate: datetime):
        self.tokenID = tokenID
        self.userID = userID
        self.tokenValue = tokenValue
        self.expiryDate = expiryDate

class Label:
    def __init__(self,
                 labelID: int,
                 name: str):
        self.labelID = labelID
        self.name = name

class TodoItem:
    def __init__(self,
                 itemID: int,
                 name: str,
                 parentID: int | None,
                 createdDate: datetime,
                 userID: int,
                 itemType: str,
                 labelID: int | None):
        self.itemID = itemID
        self.name = name
        self.parentID = parentID
        self.createdDate = createdDate
        self.userID = userID
        self.itemType = itemType
        self.labelID = labelID

class TaskAttributes:
    def __init__(self,
                 taskID: int,
                 dueDate: datetime | None,
                 priority: str,
                 status: str,
                 description: str,
                 inTodayDate: datetime):
        self.taskID = taskID
        self.dueDate = dueDate
        self.priority = priority
        self.status = status
        self.description = description
        self.inTodayDate = inTodayDate

class Media:
    def __init__(self,
                 mediaID: int,
                 fileURL: str,
                 taskID: int,
                 uploadedDate: datetime):
        self.mediaID = mediaID
        self.fileURL = fileURL
        self.taskID = taskID
        self.uploadedDate = uploadedDate

class Logs:
    def __init__(self,
                 logID: int,
                 taskID: int,
                 logContent: str,
                 createdAt: datetime):
        self.logID = logID
        self.taskID = taskID
        self.logContent = logContent
        self.createdAt = createdAt

class Reminder:
    def __init__(self,
                 reminderID: int,
                 taskID: int,
                 reminderMode: str,
                 timeOffset: timedelta,
                 specificTime: datetime | None):
        self.reminderID = reminderID
        self.taskID = taskID
        self.reminderMode = reminderMode
        self.timeOffset = timeOffset
        self.specificTime = specificTime

class PomodoroHistory:
    def __init__(self,
                 pomodoroID: int,
                 taskID: int,
                 startTime: datetime,
                 duration: timedelta,
                 endTime: datetime,
                 status: str,
                 createdAt: datetime):
        self.pomodoroID = pomodoroID
        self.taskID = taskID
        self.startTime = startTime
        self.duration = duration
        self.endTime = endTime
        self.status = status
        self.createdAt = createdAt