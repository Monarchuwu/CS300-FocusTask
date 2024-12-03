import bcrypt
from datetime import datetime, timedelta

from . import databases, objects
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class UserManager:
    _currentUserID = None

    def getCurrentUserID(self):
        return self._currentUserID
    
    def registerUser(self, username: str, email: str, password: str, avatarURL: str | None):
        passwordHash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            user = databases.UserDB(username=username, email=email, passwordHash=passwordHash, avatarURL=avatarURL)
            user.save()
            return "User registered successfully"
        except IntegrityError:
            raise ValueError("Error: Email already exists")

    def signIn(self, email: str, password: str):
        try:
            user = databases.UserDB.objects.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.passwordHash.encode('utf-8')):
                self._currentUserID = user.userID
                return "Sign-in successful"
            else:
                raise ValueError("Error: Incorrect password")
        except ObjectDoesNotExist:
            raise ValueError("Error: User not found")

    def signOut(self):
        if self._currentUserID is None:
            raise ValueError("Error: No user signed in")
        self._currentUserID = None
        return "Sign-out successful"

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
                parentID=None if task.parentID is None else databases.TodoItemDB.objects.get(itemID=task.parentID),
                createdDate=datetime.now(), # ignore the createdDate from the input
                userID=databases.UserDB.objects.get(userID=task.userID),
                itemType=task.itemType,
                labelID=None if task.labelID is None else databases.LabelDB.objects.get(labelID=task.labelID)
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
            raise ValueError(f"An error occurred while adding the task: {e} parentID is {task.parentID}")

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
        try:
            current_user = UserManager.getCurrentUserID()
            records = databases.WebsiteBlockingDB.objects.filter(UserID=current_user)
            return [record.get_data_object() for record in records]
        except Exception as e:
            print(f"Error fetching block list: {e}")
            return []

    def addToBlockList(self, URL: str):
        try:
            current_user = UserManager.getCurrentUserID()
            new_block = databases.WebsiteBlockingDB(URL=URL, UserID=current_user)
            new_block.save()
            return f"Website '{URL}' added to block list."
        except IntegrityError:
            raise ValueError(f"Website {URL} already in block list")
        except Exception as e:
            raise ValueError(f"Error adding to block list: {e}")

    def deleteFromBlockList(self, blockID: int):
        try:
            current_user = UserManager.getCurrentUserID()
            databases.WebsiteBlockingDB.objects.filter(blockID=blockID, UserID=current_user).delete()
            return f"BlockID {blockID} removed from block list."
        except Exception as e:
            raise ValueError(f"Error deleting from block list: {e}")

    # toggle website blocking status
    def toggleBlock(self, blockID: int):
        try:
            current_user = UserManager.getCurrentUserID()
            block_entry = databases.WebsiteBlockingDB.objects.get(blockID=blockID, UserID=current_user)
            block_entry.isBlocking = not block_entry.isBlocking
            block_entry.save()
            return f"BlockID {blockID} toggled to {'blocking' if block_entry.isBlocking else 'not blocking'}."
        except databases.WebsiteBlockingDB.DoesNotExist:
            raise ValueError(f"BlockID {blockID} does not exist.")
        except Exception as e:
            raise ValueError(f"Error toggling block status: {e}")

    def setBlock(self, blockID: int, status: bool):
        try:
            current_user = UserManager.getCurrentUserID()
            block_entry = databases.WebsiteBlockingDB.objects.get(blockID=blockID, UserID=current_user)
            block_entry.isBlocking = status
            block_entry.save()
            return f"BlockID {blockID} set to {'blocking' if status else 'not blocking'}."
        except databases.WebsiteBlockingDB.DoesNotExist:
            raise ValueError(f"BlockID {blockID} does not exist.")
        except Exception as e:
            raise ValueError(f"Error setting block status: {e}")

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

class PomodoroManager:
    class Status:
        RUNNING = "Running"
        PAUSED = "Paused"
        ENDED = "Ended"

    def setTaskID(self, taskID: int):
        try:
            task = databases.TodoItemDB.objects.get(taskID = taskID)
            if (task):
                databases.PomodoroHistoryDB.objects.create(
                    taskID = taskID,
                    startTime = None,
                    duration = None,
                    endTime = None,
                    status = databases.PomodoroHistoryDB.Status.CANCELED,
                    createdAt = datetime.now()
                )
            
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Task ID {taskID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while checking the taskID for pomodoro: {taskID}") 

    def setTime(self, pomodoroID: int, length: timedelta):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            pomodoro.duration = length
            pomodoro.currentDuration = length
            pomodoro.save()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while setting duration for pomodoro with ID: {pomodoroID}") 

    def start(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            if pomodoro.status == databases.PomodoroHistoryDB.Status.CANCELED:
                pomodoro.startTime = datetime.now()
                pomodoro.endTime = pomodoro.startTime
                pomodoro.status = databases.PomodoroHistoryDB.Status.RUNNING
                pomodoro.save()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while starting timer for pomodoro with ID: {pomodoroID}")

    def unpause(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            if pomodoro.status == databases.PomodoroHistoryDB.Status.PAUSED:
                pomodoro.endTime = datetime.now()
                pomodoro.status = databases.PomodoroHistoryDB.Status.RUNNING
                pomodoro.save()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while continuing timer for pomodoro with ID: {pomodoroID}")
        

    def pause(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            if pomodoro.status == databases.PomodoroHistoryDB.Status.RUNNING:
                pomodoro.status = databases.PomodoroHistoryDB.Status.PAUSED
                elapsed = datetime.now() - pomodoro.endTime
                pomodoro.currentDuration -= elapsed
                pomodoro.endTime = None
                pomodoro.save()
                if (pomodoro.currentDuration <= timedelta()):
                    self.end(pomodoroID)
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while pausing timer for pomodoro with ID {pomodoroID}: {e}")

    def getTime(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            elapsed = (now:=datetime.now()) - pomodoro.endTime
            pomodoro.currentDuration -= elapsed
            pomodoro.endTime = now
            pomodoro.save()
            if (pomodoro.currentDuration <= timedelta()):
                self.end(pomodoroID)
            return max(pomodoro.currentDuration, timedelta())
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while getting timer for pomodoro with ID {pomodoroID}: {e}")

    def end(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            pomodoro.status = databases.PomodoroHistoryDB.Status.COMPLETED
            pomodoro.save()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while ending timer for pomodoro with ID: {pomodoroID}")

    def getStatus(self, pomodoroID: int):
        return self.status