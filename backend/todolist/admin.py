from django.contrib import admin
from .models import databases

# Register your models here.
admin.site.register(databases.UserDB)
admin.site.register(databases.WebsiteBlockingDB)
admin.site.register(databases.PreferencesDB)
admin.site.register(databases.AuthenticationTokenDB)
admin.site.register(databases.LabelDB)
admin.site.register(databases.TodoItemDB)
admin.site.register(databases.TaskAttributesDB)
admin.site.register(databases.MediaDB)
admin.site.register(databases.LogsDB)
admin.site.register(databases.ReminderDB)
admin.site.register(databases.PomodoroHistoryDB)