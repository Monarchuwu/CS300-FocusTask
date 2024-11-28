from datetime import datetime, timedelta
from . import databases, objects

class UserManager:
    currentUserID = None

    def getCurrentUserID(self):
        return self.currentUserID
    
    def registerUser(self, username: str, email: str, password: str, avatarURL: str | None):
        pass

    def signIn(self, email: str, password: str):
        pass

    def signOut(self):
        pass

class TaskManager:
    def getTaskList(self, projectID: int):
        pass

    def addTask(self, task: objects.TodoItem):
        pass

    def deleteTask(self, taskID: int):
        pass

    def editTask(self, task: objects.TodoItem):
        pass

    # toggle task status between pending and completed
    def toggleTask(self, taskID: int):
        pass

    def getTodayTaskList(self):
        pass

    def addTaskToToday(self, taskID: int):
        pass

    def removeTaskFromToday(self, taskID: int):
        pass

    def suggestTodayTask(self):
        pass

class WebsiteBlockingManager:
    def getBlockList(self):
        pass

    def addToBlockList(self, URL: str):
        pass

    def deleteFromBlockList(self, blockID: int):
        pass

    # toggle website blocking status
    def toggleBlock(self, blockID: int):
        pass

    def setBlock(self, blockID: int, status: bool):
        pass

class PreferencesManager:
    def setLanguage(self, language: str):
        pass

    def setTimezone(self, timezone: str):
        pass

    def setNotification(self, status: bool):
        pass

    def setAutoBlock(self, status: bool):
        pass

    def getLanguage(self):
        pass

    def getTimezone(self):
        pass

    def getNotification(self):
        pass

    def getAutoBlock(self):
        pass

# start, pause, end should be run asynchronously
class PomodoroManager:
    class Status:
        RUNNING = "Running"
        PAUSED = "Paused"
        ENDED = "Ended"

    startTimestamp = None # should be datetime
    status = Status.ENDED
    length = None # should be timedelta
    taskID = None

    def setTaskID(self, taskID: int):
        pass

    def setTime(self, length: timedelta):
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def end(self):
        pass

    def getStatus(self):
        pass