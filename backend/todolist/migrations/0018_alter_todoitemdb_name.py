# Generated by Django 5.1 on 2024-12-26 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0017_merge_20241223_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitemdb',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
