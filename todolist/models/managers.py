from asyncio import Task
from datetime import datetime, timedelta
from enum import Enum
from tracemalloc import start

from pytz import timezone
from yaml import StreamStartToken
from . import databases, objects
from django.db import IntegrityError

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
        try:
            tasks = databases.TodoItemDB.objects.filter(parentID=projectID)
            return [task.get_data_object() for task in tasks]
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Project with ID {projectID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching the task list: {e}")

    def addTask(self, task: objects.TodoItem):
        try:
            databases.TodoItemDB.objects.create(
                itemID=task.itemID,
                name=task.name,
                parentID=databases.TodoItemDB.objects.get(itemID=task.parentID) if task.parentID else None,
                createdDate=task.createdDate,
                userID=databases.UserDB.objects.get(userID=task.userID),
                itemType=task.itemType,
                labelID=databases.LabelDB.objects.get(labelID=task.labelID) if task.labelID else None,
            )
        except databases.UserDB.DoesNotExist:
            raise ValueError(f"User with ID {task.userID} does not exist.")
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Parent task with ID {task.parentID} does not exist.")
        except databases.LabelDB.DoesNotExist:
            raise ValueError(f"Label with ID {task.labelID} does not exist.")
        except IntegrityError:
            raise ValueError(f"A task with ID {task.itemID} already exists.")
        except Exception as e:
            raise ValueError(f"An error occurred while adding the task: {e}")

    def deleteTask(self, taskID: int):
        try:
            task = databases.TodoItemDB.objects.get(itemID=taskID)
            task.delete()
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Task with ID {taskID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while deleting the task: {e}")
        
    def editTask(self, task: objects.TodoItem):
        try:
            # Update TodoItem fields
            task_db = databases.TodoItemDB.objects.get(itemID=task.itemID)
            task_db.name = task.name
            task_db.parentID = databases.TodoItemDB.objects.get(itemID=task.parentID) if task.parentID else None
            task_db.labelID = databases.LabelDB.objects.get(labelID=task.labelID) if task.labelID else None
            task_db.save()

            # Update TaskAttributes if available
            task_attributes = databases.TaskAttributesDB.objects.get(taskID=task.itemID)
            if hasattr(task, "attributes"):
                task_attributes.dueDate = task.attributes.dueDate
                task_attributes.priority = task.attributes.priority
                task_attributes.status = task.attributes.status
                task_attributes.description = task.attributes.description
                task_attributes.inTodayDate = task.attributes.inTodayDate
                task_attributes.save()
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Task with ID {task.itemID} does not exist.")
        except databases.TaskAttributesDB.DoesNotExist:
            raise ValueError(f"TaskAttributes for task ID {task.itemID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while editing the task: {e}")


    # toggle task status between pending and completed
    def toggleTask(self, taskID: int):
        try:
            task_attr = databases.TaskAttributesDB.objects.get(taskID=taskID)
            if task_attr.status == databases.TaskAttributesDB.Status.PENDING:
                task_attr.status = databases.TaskAttributesDB.Status.COMPLETED
            else:
                task_attr.status = databases.TaskAttributesDB.Status.PENDING
            task_attr.save()
        except databases.TaskAttributesDB.DoesNotExist:
            raise ValueError(f"TaskAttributes for task ID {taskID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while toggling the task status: {e}")

    def getTodayTaskList(self):
        try:
            tasks = databases.TaskAttributesDB.objects.filter(
                inTodayDate__date=datetime.now().date()
            )
            return [task.get_data_object() for task in tasks]
        except Exception as e:
            raise ValueError(f"An error occurred while fetching today's task list: {e}")

    def addTaskToToday(self, taskID: int):
        try:
            task_attr = databases.TaskAttributesDB.objects.get(taskID=taskID)
            task_attr.inTodayDate = datetime.now()
            task_attr.save()
        except databases.TaskAttributesDB.DoesNotExist:
            raise ValueError(f"TaskAttributes for task ID {taskID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while adding the task to today's list: {e}")

    def removeTaskFromToday(self, taskID: int):
        try:
            task_attr = databases.TaskAttributesDB.objects.get(taskID=taskID)
            task_attr.inTodayDate = datetime(2100, 1, 1)  # Reset to default date
            task_attr.save()
        except databases.TaskAttributesDB.DoesNotExist:
            raise ValueError(f"TaskAttributes for task ID {taskID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while removing the task from today's list: {e}")


    def suggestTodayTask(self):
        try:
            now = datetime.now()

            # 1. Overdue tasks
            overdue_tasks = databases.TaskAttributesDB.objects.filter(
                status=databases.TaskAttributesDB.Status.PENDING,
                dueDate__lt=now
            ).order_by("priority", "dueDate")

            # 2. Tasks due today
            today_tasks = databases.TaskAttributesDB.objects.filter(
                status=databases.TaskAttributesDB.Status.PENDING,
                dueDate__date=now.date()
            ).order_by("priority", "dueDate")

            # 3. Previously added to today's list but not completed
            in_today_tasks = databases.TaskAttributesDB.objects.filter(
                status=databases.TaskAttributesDB.Status.PENDING,
                inTodayDate__lt=now,
                inTodayDate__date=now.date()
            ).order_by("inTodayDate")

            # 4. Recently added tasks
            recently_added_tasks = databases.TaskAttributesDB.objects.filter(
                status=databases.TaskAttributesDB.Status.PENDING
            ).order_by("-taskID")

            # Combine the task lists in order of priority
            suggested_tasks = list(overdue_tasks) + list(today_tasks) + list(in_today_tasks) + list(recently_added_tasks)

            # Remove duplicates and keep order
            unique_suggested_tasks = []
            seen = set()
            for task in suggested_tasks:
                if task.taskID not in seen:
                    seen.add(task.taskID)
                    unique_suggested_tasks.append(task)

            return [task.get_data_object() for task in unique_suggested_tasks]
        except Exception as e:
            raise ValueError(f"An error occurred while suggesting tasks for today: {e}")


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
    def setLanguage(self, userID: int, language: databases.PreferencesDB.Language):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            preference.language = language
            preference.save()
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while changing the preferred language of userID: {userID}") 
        

    def setTimezone(self, userID: int, timezone: databases.PreferencesDB.Timezone):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            preference.timezone = timezone
            preference.save()
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while changing the preferred timezone of userID: {userID}") 

    def setNotification(self, userID: int, status: bool):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            preference.notification = status
            preference.save()
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while changing the preferred notification of userID: {userID}") 

    def setAutoBlock(self, userID: int, status: bool):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            preference.autoBlock = status
            preference.save()
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while changing the preferred auto block of userID: {userID}") 

    def getLanguage(self, userID: int):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            return preference.language
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while getting the preferred language of userID: {userID}") 

    def getTimezone(self, userID: int):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            return preference.timezone
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while getting the preferred timezone of userID: {userID}") 

    def getNotification(self, userID: int):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            return preference.notification
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while getting the preferred notification of userID: {userID}") 

    def getAutoBlock(self, userID: int):
        try:
            preference = databases.PreferencesDB.objects.get(userID = userID)
            return preference.autoBlock
        except databases.PreferencesDB.DoesNotExist:
            raise ValueError(f"Preference for user ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while getting the preferred auto block of userID: {userID}") 

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
        try:
            task = databases.TodoItemDB.objects.get(taskID = taskID)
            if (task):
                self.taskID = taskID
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Preference for task ID {taskID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while checking the taskID: {taskID}") 

    def setTime(self, length: timedelta):
        self.length = length

    def start(self):
        self.startTimestamp = datetime.now()
        self.status = PomodoroManager.Status.RUNNING

    def pause(self):
        self.status = PomodoroManager.Status.PAUSED

    def end(self):
        self.status = PomodoroManager.Status.ENDED
        databases.PomodoroHistoryDB.objects.create(
            pomodoroID = int(datetime.now()),
            taskID = self.taskID,
            startTime = self.startTimestamp,
            duration = self.length,
            endTime = datetime.now(),
            status = databases.PomodoroHistoryDB.Status.COMPLETED,
            createdAt = datetime.now()
        )

    def getStatus(self):
        return self.status