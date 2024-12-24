import bcrypt
from datetime import datetime, timedelta
from django.utils import timezone

from . import databases, objects
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class UserManager:
    def getUserID(self, authenticationToken: str):
        try:
            token = databases.AuthenticationTokenDB.objects.get(tokenValue=authenticationToken)
            if token.expiryDate < timezone.now():
                token.delete()
                raise ValueError("Error: Authentication token expired")
            return token.userID.userID
        except databases.AuthenticationTokenDB.DoesNotExist:
            raise ValueError("Error: Authentication token not found")
    
    def registerUser(self, username: str, email: str, password: str, avatarURL: str = None):
        passwordHash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        passwordHash = passwordHash.decode('utf-8')
        try:
            if databases.UserDB.objects.filter(email=email).exists():
                raise ValueError("Error: Email already exists")
            user = databases.UserDB(username=username, email=email, passwordHash=passwordHash, avatarURL=avatarURL)
            user.save()
            return "User registered successfully"
        except Exception as e:
            raise ValueError(f"An error occurred while registering the new user: {e}")

    def signIn(self, email: str, password: str):
        try:
            user = databases.UserDB.objects.get(email=email)
            if not bool(bcrypt.checkpw(password.encode('utf-8'), user.passwordHash.encode('utf-8'))):
                raise ValueError("Error: Incorrect password")
        except ObjectDoesNotExist:
            raise ValueError("Error: User not found")
        
        # Create a new authentication token
        token = bcrypt.gensalt().decode('utf-8')
        databases.AuthenticationTokenDB.objects.create(userID=user, tokenValue=token, expiryDate=timezone.now() + timedelta(days=1))
        return token

    def signOut(self, authenticationToken: str):
        try:
            databases.AuthenticationTokenDB.objects.get(tokenValue=authenticationToken).delete()
            return "User signed out successfully"
        except databases.AuthenticationTokenDB.DoesNotExist:
            raise ValueError("Error: Authentication token not found")


class TaskManager:
    def getTaskList(self, projectID: int):
        try:
            tasks = databases.TodoItemDB.objects.filter(parentID=projectID)
            return [task.get_data_object() for task in tasks]
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Project with ID {projectID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching the task list: {e}")

    def addTodoItem(self, todoItem: objects.TodoItem):
        try:
            item = databases.TodoItemDB(
                name=todoItem.name,
                parentID=None if todoItem.parentID is None else databases.TodoItemDB.objects.get(itemID=todoItem.parentID),
                userID=databases.UserDB.objects.get(userID=todoItem.userID),
                createdDate=timezone.now() if todoItem.createdDate is None else todoItem.createdDate,
                itemType=todoItem.itemType,
                labelID=None if todoItem.labelID is None else databases.LabelDB.objects.get(labelID=todoItem.labelID)
            )
            item.full_clean()
            item.save()
            return item.get_data_object()
        except databases.UserDB.DoesNotExist:
            raise ValueError(f"User with ID {todoItem.userID} does not exist.")
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Parent todo item with ID {todoItem.parentID} does not exist.")
        except databases.LabelDB.DoesNotExist:
            raise ValueError(f"Label with ID {todoItem.labelID} does not exist.")
        except IntegrityError:
            raise ValueError(f"A todo item with ID {todoItem.itemID} already exists.")
        except Exception as e:
            raise ValueError(f"An error occurred while adding the todo item: {e} parentID is {todoItem.parentID}")

    def deleteTodoItem(self, itemID: int):
        try:
            item = databases.TodoItemDB.objects.get(itemID=itemID)
            item.delete()
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Todo Item with ID {itemID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while deleting the todo item: {e}")
        
    def editTodoItem(self, todoItem: objects.TodoItem):
        try:
            # Update TodoItem fields
            item_db = databases.TodoItemDB.objects.get(itemID=todoItem.itemID)
            item_db.name = todoItem.name
            item_db.parentID = databases.TodoItemDB.objects.get(itemID=todoItem.parentID) if todoItem.parentID else None
            item_db.labelID = databases.LabelDB.objects.get(labelID=todoItem.labelID) if todoItem.labelID else None
            item_db.save()
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Todo Item with ID {item_db.itemID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while editing the task: {e}")

    def getTodoItem(self, itemID: int):
        try:
            item = databases.TodoItemDB.objects.get(itemID=itemID)
            return item.get_data_object()
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Todo Item with ID {itemID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching the todo item: {e}")

    def getAllTodoItem(self, userID: int):
        try:
            items = databases.TodoItemDB.objects.filter(userID=userID)
            return [item.get_data_object() for item in items]
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"User with ID {userID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching all the todo items: {e}")

    def getAllProject(self, userID: int):
        try:
            items = databases.TodoItemDB.objects.filter(userID=userID, itemType=databases.TodoItemDB.ItemType.PROJECT)
            return [item.get_data_object() for item in items]
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"User with ID {userID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching all the todo items: {e}")

    def addTaskAttributes(self, attrs: objects.TaskAttributes):
        try:
            taskAttributes_db = databases.TaskAttributesDB(
                taskID=databases.TodoItemDB.objects.get(itemID=attrs.taskID),
                dueDate=attrs.dueDate,
                priority=attrs.priority,
                status=attrs.status,
                description=attrs.description,
                inTodayDate=attrs.inTodayDate
            )
            taskAttributes_db.full_clean()
            taskAttributes_db.save()
            return taskAttributes_db.get_data_object()
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Todo Item with ID {attrs.taskID} does not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while adding the task attributes: {e}")

    def deteleTaskAttributes(self, taskID: int):
        try:
            task_attr = databases.TaskAttributesDB.objects.get(taskID=taskID)
            task_attr.delete()
        except databases.TaskAttributesDB.DoesNotExist:
            raise ValueError(f"TaskAttributes for task ID {taskID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while deleting the task attributes: {e}")

    def getTaskAttributes(self, taskID: int):
        try:
            task_attr = databases.TaskAttributesDB.objects.get(taskID=taskID)
            return task_attr.get_data_object()
        except databases.TaskAttributesDB.DoesNotExist:
            raise ValueError(f"TaskAttributes for task ID {taskID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while fetching the task attributes: {e}")

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

    def getTodayTaskList(self, userID: int):
        try:
            tasks = databases.TaskAttributesDB.objects.filter(
                taskID__userID__userID=userID,
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
            return task_attr.get_data_object()
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

    def suggestTodayTask(self, userID: int):
        try:
            now = datetime.now()

            # 1. Overdue tasks
            overdue_tasks = databases.TaskAttributesDB.objects.filter(
                taskID__userID__userID=userID,
                status=databases.TaskAttributesDB.Status.PENDING,
                dueDate__lt=now
            ).exclude(
                inTodayDate__date=now.date()
            ).order_by("priority", "dueDate")

            # 2. Tasks due today
            today_tasks = databases.TaskAttributesDB.objects.filter(
                taskID__userID__userID=userID,
                status=databases.TaskAttributesDB.Status.PENDING,
                dueDate__date=now.date()
            ).exclude(
                inTodayDate__date=now.date()
            ).order_by("priority", "dueDate")

            # 3. Previously added to today's list but not completed
            in_today_tasks = databases.TaskAttributesDB.objects.filter(
                taskID__userID__userID=userID,
                status=databases.TaskAttributesDB.Status.PENDING,
                inTodayDate__date__lt=now.date()
            ).order_by("inTodayDate")

            # 4. Recently added tasks
            recently_added_tasks = databases.TaskAttributesDB.objects.filter(
                taskID__userID__userID=userID,
                status=databases.TaskAttributesDB.Status.PENDING
            ).exclude(
                inTodayDate__date=now.date()
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
    def getBlockList(self, userID: int):
        try:
            records = databases.WebsiteBlockingDB.objects.filter(UserID=userID)
            return [record.get_data_object() for record in records]
        except Exception as e:
            print(f"Error fetching block list: {e}")
            return []
        
    def getBlockingURLs(self, userID: int):
        try:
            records = databases.WebsiteBlockingDB.objects.filter(UserID=userID, isBlocking=True)
            return [record.URL for record in records]
        except Exception as e:
            print(f"Error fetching block URLs: {e}")

    def addToBlockList(self, userID: int, URL: str):
        try:
            new_block = databases.WebsiteBlockingDB(URL=URL, UserID=userID)
            new_block.save()
            return f"Website '{URL}' added to block list."
        except IntegrityError:
            raise ValueError(f"Website {URL} already in block list")
        except Exception as e:
            raise ValueError(f"Error adding to block list: {e}")

    def deleteFromBlockList(self, userID: int, blockID: int):
        try:
            databases.WebsiteBlockingDB.objects.filter(blockID=blockID, UserID=userID).delete()
            return f"BlockID {blockID} removed from block list."
        except Exception as e:
            raise ValueError(f"Error deleting from block list: {e}")

    # toggle website blocking status
    def toggleBlock(self, userID: int, blockID: int):
        try:
            block_entry = databases.WebsiteBlockingDB.objects.get(blockID=blockID, UserID=userID)
            block_entry.isBlocking = not block_entry.isBlocking
            block_entry.save()
            return f"BlockID {blockID} toggled to {'blocking' if block_entry.isBlocking else 'not blocking'}."
        except databases.WebsiteBlockingDB.DoesNotExist:
            raise ValueError(f"BlockID {blockID} does not exist.")
        except Exception as e:
            raise ValueError(f"Error toggling block status: {e}")

    def setBlock(self, userID: int, blockID: int, status: bool):
        try:
            block_entry = databases.WebsiteBlockingDB.objects.get(blockID=blockID, UserID=userID)
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

    def get_pomodoro_list(self, userID: int):
        try:
            pomodoros = databases.PomodoroHistoryDB.objects.filter(
                taskID__userID__userID=userID                          # Ensure the Pomo belongs to a Task of the specified User
            )
            return [pomodoro.get_data_object() for pomodoro in pomodoros]
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"TodoItem with userID {userID} do not exist.")
        except databases.UserDB.DoesNotExist:
            raise ValueError(f"User ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while checking the userID {userID} for pomodoro") 

    def checkRunningPomodoro(self, userID: int):
        try:
            return databases.PomodoroHistoryDB.objects.filter(
                taskID__userID__userID=userID,                          # Ensure the Pomo belongs to a Task of the specified User
                status = databases.PomodoroHistoryDB.Status.RUNNING     # Check for the specific value of status
            ).exists()
            
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"TodoItem with userID {userID} do not exist.")
        except databases.UserDB.DoesNotExist:
            raise ValueError(f"User ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while checking the userID {userID} for pomodoro") 

    def checkUserAccessToPomodoro(self, userID: int, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID=pomodoroID)
            task = databases.TodoItemDB.objects.filter(userID=userID, itemID=pomodoro.taskID.itemID)
            return task.exists()
            
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"TodoItem with userID {userID} and pomodoroID {pomodoroID} do not exist.")
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory ID {pomodoroID} do not exist.")
        except Exception as e:
            print(e)
            raise ValueError(f"An error occurred while checking the userID {userID} for pomodoroID: {pomodoroID}") 

    def setTaskID(self, taskID: int):
        try:
            task = databases.TodoItemDB.objects.get(itemID = taskID)
            if (task):
                pomodoroList = databases.PomodoroHistoryDB.objects.filter(taskID__itemID=taskID).exclude(status=databases.PomodoroHistoryDB.Status.COMPLETED)
                if pomodoroList.exists():
                    return pomodoroList.first().get_data_object()
                pomodoro = databases.PomodoroHistoryDB.objects.create(
                    taskID = task,
                    startTime = None,
                    duration = None,
                    currentDuration = None,
                    endTime = None,
                    status = databases.PomodoroHistoryDB.Status.CANCELED,
                    createdAt = timezone.now()
                )
                return pomodoro.get_data_object()
            
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"Task ID {taskID} do not exist.")
        except Exception as e:
            print(e)
            raise ValueError(f"An error occurred while checking the taskID for pomodoro: {taskID}") 

    def setTime(self, pomodoroID: int, length: timedelta):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            pomodoro.duration = length
            pomodoro.currentDuration = length
            pomodoro.save()
            return pomodoro.get_data_object()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while setting duration for pomodoro with ID: {pomodoroID}") 

    def start(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            if pomodoro.status == databases.PomodoroHistoryDB.Status.CANCELED:
                pomodoro.startTime = timezone.now()
                pomodoro.endTime = pomodoro.startTime
                if pomodoro.intervals is None:
                    pomodoro.intervals = []
                pomodoro.intervals.append(pomodoro.startTime.isoformat())
                pomodoro.status = databases.PomodoroHistoryDB.Status.RUNNING
                pomodoro.save()
            return pomodoro.get_data_object()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while starting timer for pomodoro with ID: {pomodoroID}")

    def unpause(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            if pomodoro.status == databases.PomodoroHistoryDB.Status.PAUSED:
                pomodoro.endTime = timezone.now()
                pomodoro.intervals.append(pomodoro.endTime.isoformat())
                pomodoro.status = databases.PomodoroHistoryDB.Status.RUNNING
                pomodoro.save()
            return pomodoro.get_data_object()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while continuing timer for pomodoro with ID: {pomodoroID}")
        

    def pause(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            if pomodoro.status == databases.PomodoroHistoryDB.Status.RUNNING:
                pomodoro.status = databases.PomodoroHistoryDB.Status.PAUSED
                elapsed = timezone.now() - pomodoro.endTime
                pomodoro.currentDuration -= elapsed
                pomodoro.endTime += elapsed
                pomodoro.intervals.append(pomodoro.endTime.isoformat())
                pomodoro.save()
            return pomodoro.get_data_object()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while pausing timer for pomodoro with ID {pomodoroID}: {e}")

    def getTime(self, pomodoroID: int):
        try:
            pomodoro = databases.PomodoroHistoryDB.objects.get(pomodoroID = pomodoroID)
            if pomodoro.status == databases.PomodoroHistoryDB.Status.RUNNING:
                elapsed = (now:=timezone.now()) - pomodoro.endTime
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
            pomodoro.currentDuration = timedelta()
            pomodoro.endTime = timezone.now()
            pomodoro.intervals.append(pomodoro.endTime.isoformat())
            pomodoro.save()
            return pomodoro.get_data_object()
        except databases.PomodoroHistoryDB.DoesNotExist:
            raise ValueError(f"PomodoroHistory with ID {pomodoroID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while ending timer for pomodoro with ID: {pomodoroID}")

    def get_hour_list(self, userID: int, hour: datetime):
        try:
            hour_start = hour
            hour_end = hour + timedelta(hours=1)

            run_time = timedelta()
            pause_time = timedelta()

            pomodoros = databases.PomodoroHistoryDB.objects.filter(taskID__userID__userID=userID, status=databases.PomodoroHistoryDB.Status.COMPLETED)
            
            for pomodoro in pomodoros:
                for i, (start_time, end_time) in enumerate(zip(pomodoro.intervals[:-1], pomodoro.intervals[1:])):
                    overlap_start = max(datetime.fromisoformat(start_time), hour_start.astimezone())
                    overlap_end = min(datetime.fromisoformat(end_time), hour_end.astimezone())
                    if overlap_start < overlap_end:
                        if i % 2 == 0:
                            run_time += overlap_end - overlap_start
                        else:
                            pause_time += overlap_end - overlap_start
            return (run_time.total_seconds(), pause_time.total_seconds())
        except Exception as e:
            raise ValueError(f"An error occured while getting the hour stats for userID {userID} in hour {hour.isoformat()}: {e}")
    def get_day_list(self, userID: int, date: datetime):
        date_start = date
        date_end = date + timedelta(days=1)

        run_time = timedelta()
        pause_time = timedelta()

        pomodoros = databases.PomodoroHistoryDB.objects.filter(taskID__userID__userID=userID, status=databases.PomodoroHistoryDB.Status.COMPLETED)
        for pomodoro in pomodoros:
            for i, (start_time, end_time) in enumerate(zip(pomodoro.intervals[:-1], pomodoro.intervals[1:])):
                overlap_start = max(start_time, date_start)
                overlap_end = min(end_time, date_end)
                if overlap_start < overlap_end:
                    if i % 2 == 0:
                        run_time += overlap_end - overlap_start
                    else:
                        pause_time += overlap_end - overlap_start
        return (run_time, pause_time)

    def getStatus(self, pomodoroID: int):
        return self.status
    
    def getLastActiveSession(self, userID: int):
        try:
            pomodoros = databases.PomodoroHistoryDB.objects.filter(
                taskID__userID__userID=userID,
                status=databases.PomodoroHistoryDB.Status.RUNNING
            )
            if not pomodoros.exists():
                pomodoros = databases.PomodoroHistoryDB.objects.filter(
                    taskID__userID__userID=userID,
                    status=databases.PomodoroHistoryDB.Status.PAUSED
                ).order_by('-endTime')
            
            if pomodoros.exists():
                return pomodoros.first().get_data_object()
            return None
        except databases.TodoItemDB.DoesNotExist:
            raise ValueError(f"TodoItem with userID {userID} do not exist.")
        except databases.UserDB.DoesNotExist:
            raise ValueError(f"User ID {userID} do not exist.")
        except Exception as e:
            raise ValueError(f"An error occurred while checking the userID {userID} for pomodoro")