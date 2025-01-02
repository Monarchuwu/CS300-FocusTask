from django.db import migrations
from ..models.databases import TodoItemDB

# for all old users, we will add a new project with an empty name


def add_empty_name_project_section(apps, schema_editor):
    UserDBModel = apps.get_model("todolist", "UserDB")
    TodoItemDBModel = apps.get_model("todolist", "TodoItemDB")
    for user in UserDBModel.objects.all():
        # check if the user has a name-empty project
        if not TodoItemDBModel.objects.filter(name="", userID=user, itemType=TodoItemDB.ItemType.PROJECT).exists():
            TodoItemDBModel.objects.create(
                name="",
                userID=user,
                itemType=TodoItemDB.ItemType.PROJECT
            )
    for projectItem in TodoItemDBModel.objects.filter(itemType=TodoItemDB.ItemType.PROJECT):
        # check if the project has a name-empty section
        if not TodoItemDBModel.objects.filter(name="", userID=projectItem.userID, parentID=projectItem, itemType=TodoItemDB.ItemType.SECTION).exists():
            TodoItemDBModel.objects.create(
                name="",
                userID=projectItem.userID,
                parentID=projectItem,
                itemType=TodoItemDB.ItemType.SECTION
            )


def remove_empty_name_project_section(apps, schema_editor):
    TodoItemDBModel = apps.get_model("todolist", "TodoItemDB")
    TodoItemDBModel.objects.filter(
        name="", itemType=TodoItemDB.ItemType.PROJECT).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0018_alter_todoitemdb_name'),
    ]

    operations = [
        migrations.RunPython(code=add_empty_name_project_section,
                             reverse_code=remove_empty_name_project_section),
    ]
