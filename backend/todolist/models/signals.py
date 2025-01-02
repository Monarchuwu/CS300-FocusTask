from django.db.models.signals import post_save
from django.dispatch import receiver
from .databases import UserDB, TodoItemDB

# Create an empty project when a user is created
@receiver(post_save, sender=UserDB)
def create_empty_project(sender, instance, created, **kwargs):
    if created:
        TodoItemDB.objects.create(
            name="",
            userID=instance,
            itemType=TodoItemDB.ItemType.PROJECT
        )

# Create an empty section when a project is created
@receiver(post_save, sender=TodoItemDB)
def create_empty_section(sender, instance, created, **kwargs):
    if created and instance.itemType == TodoItemDB.ItemType.PROJECT:
        TodoItemDB.objects.create(
            name="",
            userID=instance.userID,
            parentID=instance,
            itemType=TodoItemDB.ItemType.SECTION
        )
