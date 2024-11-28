from django.contrib import admin
from .models import (
    UserDB, 
    WebsiteBlockingDB,
    PreferencesDB,
    AuthenticationDB,
    LabelDB,
    TodoItemDB,
    TaskAttributesDB,
    MediaDB,
    LogsDB,
    ReminderDB,
    PomodoroHistoryDB
)

# Register your models here.
admin.site.register(UserDB)
admin.site.register(WebsiteBlockingDB)
admin.site.register(PreferencesDB)
admin.site.register(AuthenticationDB)
admin.site.register(LabelDB)
admin.site.register(TodoItemDB)
admin.site.register(TaskAttributesDB)
admin.site.register(MediaDB)
admin.site.register(LogsDB)
admin.site.register(ReminderDB)
admin.site.register(PomodoroHistoryDB)