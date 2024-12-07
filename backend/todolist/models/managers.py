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
        except databases.UserDB.DoesNotExist:
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
            todoItem = databases.TodoItemDB.objects.create(
                name=todoItem.name,
                parentID=None if todoItem.parentID is None else databases.TodoItemDB.objects.get(itemID=todoItem.parentID),
                userID=databases.UserDB.objects.get(userID=todoItem.userID),
                itemType=todoItem.itemType,
                labelID=None if todoItem.labelID is None else databases.LabelDB.objects.get(labelID=todoItem.labelID)
            )
            return todoItem.get_data_object()
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

    #def addTaskAttributes(self, todoItem: objects.TodoItem):
    #    try:
    #        databases.TodoItemDB.objects.create(
    #            name=todoItem.name,
    #            parentID=None if todoItem.parentID is None else databases.TodoItemDB.objects.get(itemID=todoItem.parentID),
    #            createdDate=datetime.now(), # ignore the createdDate from the input
    #            userID=databases.UserDB.objects.get(userID=todoItem.userID),
    #            itemType=todoItem.itemType,
    #            labelID=None if todoItem.labelID is None else databases.LabelDB.objects.get(labelID=todoItem.labelID)
    #        )
    #    except databases.UserDB.DoesNotExist:
    #        raise ValueError(f"User with ID {todoItem.userID} does not exist.")
    #    except databases.TodoItemDB.DoesNotExist:
    #        raise ValueError(f"Parent todo item with ID {todoItem.parentID} does not exist.")
    #    except databases.LabelDB.DoesNotExist:
    #        raise ValueError(f"Label with ID {todoItem.labelID} does not exist.")
    #    except IntegrityError:
    #        raise ValueError(f"A todo item with ID {todoItem.itemID} already exists.")
    #    except Exception as e:
    #        raise ValueError(f"An error occurred while adding the todo item: {e} parentID is {todoItem.parentID}")

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

    #def editTodoItem(self, todoItem: objects.TodoItem):
    #    try:
    #        # Update TodoItem fields
    #        item_db = databases.TodoItemDB.objects.get(itemID=todoItem.itemID)
    #        item_db.name = todoItem.name
    #        item_db.parentID = databases.TodoItemDB.objects.get(itemID=todoItem.parentID) if todoItem.parentID else None
    #        item_db.labelID = databases.LabelDB.objects.get(labelID=todoItem.labelID) if todoItem.labelID else None
    #        item_db.save()

    #        # Update TaskAttributes if available
    #        task_attributes = databases.TaskAttributesDB.objects.get(taskID=task.itemID)
    #        if hasattr(task, "attributes"):
    #            task_attributes.dueDate = task.attributes.dueDate
    #            task_attributes.priority = task.attributes.priority
    #            task_attributes.status = task.attributes.status
    #            task_attributes.description = task.attributes.description
    #            task_attributes.inTodayDate = task.attributes.inTodayDate
    #            task_attributes.save()
    #    except databases.TodoItemDB.DoesNotExist:
    #        raise ValueError(f"Task with ID {task.itemID} does not exist.")
    #    except databases.TaskAttributesDB.DoesNotExist:
    #        raise ValueError(f"TaskAttributes for task ID {task.itemID} do not exist.")
    #    except Exception as e:
    #        raise ValueError(f"An error occurred while editing the task: {e}")

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
    def getBlockList(self, userID: int):
        try:
            records = databases.WebsiteBlockingDB.objects.filter(UserID=userID)
            return [record.get_data_object() for record in records]
        except Exception as e:
            print(f"Error fetching block list: {e}")
            return []

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