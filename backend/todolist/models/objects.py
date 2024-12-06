from datetime import datetime, timedelta
import json

def value_in_dict(dict: dict, key: str, default = None):
    if key not in dict or key.lower() == "none" or key.lower() == "null":
        return default
    return dict[key]

def normalize_data(dict: dict, required_keys: list = []):
    for key in required_keys:
        dict[key] = value_in_dict(dict, key)
    return dict

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

    def __str__(self) -> str:
        json_data = {
            "userID": self.userID,
            "username": self.username,
            "email": self.email,
            "passwordHash": self.passwordHash,
            "avatarURL": self.avatarURL,
            "createdAt": self.createdAt
        }
        return json.dumps(json_data)

    @staticmethod
    def from_json(json_data):
        json_data = normalize_data(json_data, ["userID", "username", "email", "passwordHash", "avatarURL", "createdAt"])
        return User(json_data["userID"],
                    json_data["username"],
                    json_data["email"],
                    json_data["passwordHash"],
                    json_data["avatarURL"],
                    json_data["createdAt"])

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
                 itemID: int | None,
                 name: str,
                 parentID: int | None,
                 createdDate: datetime | None,
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

    def __str__(self):
        json_data = {
            "itemID": self.itemID,
            "name": self.name,
            "parentID": self.parentID,
            "createdDate": self.createdDate.isoformat(),
            "userID": self.userID,
            "itemType": self.itemType,
            "labelID": self.labelID
        }
        return json.dumps(json_data)
    
    @staticmethod
    def from_json(json_data):
        json_data = normalize_data(json_data, ["itemID", "name", "parentID", "createdDate", "userID", "itemType", "labelID"])
        createdDate = None if json_data["createdDate"] is None else datetime.fromisoformat(json_data["createdDate"])
        return TodoItem(json_data["itemID"],
                        json_data["name"],
                        json_data["parentID"],
                        createdDate,
                        json_data["userID"],
                        json_data["itemType"],
                        json_data["labelID"])

class TaskAttributes:
    def __init__(self,
                 taskID: int,
                 dueDate: datetime = None,
                 priority: str = "Low",
                 status: str = "Pending",
                 description: str = "",
                 inTodayDate: datetime = datetime(2100, 1, 1)):
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