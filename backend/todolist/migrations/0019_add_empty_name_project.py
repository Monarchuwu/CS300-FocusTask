from django.db import migrations
from ..models.databases import TodoItemDB

# for all old users, we will add a new project with an empty name


def add_empty_name_project(apps, schema_editor):
    UserDBModel = apps.get_model("todolist", "UserDB")
    TodoItemDBModel = apps.get_model("todolist", "TodoItemDB")
    for user in UserDBModel.objects.all():
        # check if the user has a name-empty project
        instance = TodoItemDBModel.objects.create(
            name="",
            userID=user,
            itemType=TodoItemDB.ItemType.PROJECT
        )
        TodoItemDB.objects.create(
            name="",
            userID=instance.userID,
            parentID=instance,
            itemType=TodoItemDB.ItemType.SECTION
        )


# reverse 0019
def remove_empty_name_projects(apps, schema_editor):
    TodoItemDBModel = apps.get_model("todolist", "TodoItemDB")
    for project in TodoItemDBModel.objects.filter(name=""):
        project.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0018_alter_todoitemdb_name'),
    ]

    operations = [
        migrations.RunPython(add_empty_name_project,
                             remove_empty_name_projects),
    ]
