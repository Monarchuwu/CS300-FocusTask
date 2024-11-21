# Generated by Django 5.1.2 on 2024-11-04 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('taskName', models.CharField(max_length=200)),
                ('dueDate', models.DateTimeField(verbose_name='Due date')),
                ('reminder', models.DateTimeField(verbose_name='Reminding date')),
                ('repeatOne', models.BooleanField()),
                ('repeatEveryDay', models.BooleanField()),
                ('repeatEveryWeek', models.BooleanField()),
                ('description', models.CharField(max_length=500)),
            ],
        ),
    ]