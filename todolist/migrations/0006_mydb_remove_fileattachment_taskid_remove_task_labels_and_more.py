# Generated by Django 5.1 on 2024-11-28 16:53

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0005_repeatedmode_remove_label_taskid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='fileattachment',
            name='taskID',
        ),
        migrations.RemoveField(
            model_name='task',
            name='labels',
        ),
        migrations.RemoveField(
            model_name='task',
            name='repeatModeList',
        ),
        migrations.RemoveField(
            model_name='taskcontainer',
            name='tasksList',
        ),
        migrations.RemoveField(
            model_name='tasksubrelation',
            name='subTask',
        ),
        migrations.RemoveField(
            model_name='urlattachment',
            name='taskID',
        ),
        migrations.RemoveField(
            model_name='tasksubrelation',
            name='mainTask',
        ),
        migrations.CreateModel(
            name='AuthenticationTokenDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('tokenID', models.IntegerField(primary_key=True, serialize=False)),
                ('tokenValue', models.CharField(max_length=100)),
                ('expiryDate', models.DateTimeField(verbose_name='Expiry date')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='LabelDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('labelID', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='LogsDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('logID', models.IntegerField(primary_key=True, serialize=False)),
                ('logContent', models.CharField(max_length=500)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='MediaDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('mediaID', models.IntegerField(primary_key=True, serialize=False)),
                ('fileURL', models.URLField()),
                ('uploadedDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Uploaded date')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='PomodoroHistoryDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('pomodoroID', models.IntegerField(primary_key=True, serialize=False)),
                ('startTime', models.DateTimeField(verbose_name='Start time')),
                ('duration', models.DurationField()),
                ('endTime', models.DateTimeField(verbose_name='End time')),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='ReminderDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('reminderID', models.IntegerField(primary_key=True, serialize=False)),
                ('timeOffset', models.DurationField()),
                ('specificTime', models.DateTimeField(verbose_name='Specific time')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='TodoItemDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('itemID', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('createdDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date')),
                ('labelID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.labeldb')),
                ('parentID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todolist.todoitemdb')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='UserDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('userID', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('passwordHash', models.CharField(max_length=100)),
                ('avatarURL', models.URLField(null=True)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.CreateModel(
            name='WebsiteBlockingDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('blockID', models.IntegerField(primary_key=True, serialize=False)),
                ('URL', models.URLField()),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date')),
                ('isBlocking', models.BooleanField(default=True)),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.userdb')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.DeleteModel(
            name='Archive',
        ),
        migrations.DeleteModel(
            name='FileAttachment',
        ),
        migrations.DeleteModel(
            name='Label',
        ),
        migrations.DeleteModel(
            name='RepeatedMode',
        ),
        migrations.DeleteModel(
            name='TaskContainer',
        ),
        migrations.DeleteModel(
            name='URLAttachment',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.DeleteModel(
            name='TaskSubrelation',
        ),
        migrations.CreateModel(
            name='TaskAttributesDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('taskID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='todolist.todoitemdb')),
                ('dueDate', models.DateTimeField(null=True, verbose_name='Due date')),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low', max_length=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=10)),
                ('description', models.CharField(default='', max_length=500)),
                ('inTodayDate', models.DateTimeField(default=datetime.datetime(2100, 1, 1, 0, 0), verbose_name='In Today date')),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.AddField(
            model_name='reminderdb',
            name='taskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.todoitemdb'),
        ),
        migrations.AddField(
            model_name='pomodorohistorydb',
            name='taskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.todoitemdb'),
        ),
        migrations.AddField(
            model_name='mediadb',
            name='taskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.todoitemdb'),
        ),
        migrations.AddField(
            model_name='logsdb',
            name='taskID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.todoitemdb'),
        ),
        migrations.CreateModel(
            name='PreferencesDB',
            fields=[
                ('mydb_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='todolist.mydb')),
                ('userID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='todolist.userdb')),
                ('language', models.CharField(choices=[('English', 'English'), ('Vietnamese', 'Vietnamese')], default='English', max_length=20)),
                ('timezone', models.CharField(choices=[('UTC+0', 'Utc0'), ('UTC+1', 'Utc1'), ('UTC+2', 'Utc2'), ('UTC+3', 'Utc3'), ('UTC+4', 'Utc4'), ('UTC+5', 'Utc5'), ('UTC+6', 'Utc6'), ('UTC+7', 'Utc7'), ('UTC+8', 'Utc8'), ('UTC+9', 'Utc9'), ('UTC+10', 'Utc10'), ('UTC+11', 'Utc11'), ('UTC+12', 'Utc12'), ('UTC-1', 'Utc 1'), ('UTC-2', 'Utc 2'), ('UTC-3', 'Utc 3'), ('UTC-4', 'Utc 4'), ('UTC-5', 'Utc 5'), ('UTC-6', 'Utc 6'), ('UTC-7', 'Utc 7'), ('UTC-8', 'Utc 8'), ('UTC-9', 'Utc 9'), ('UTC-10', 'Utc 10'), ('UTC-11', 'Utc 11'), ('UTC-12', 'Utc 12')], default='UTC+7', max_length=10)),
                ('notification', models.BooleanField(default=False)),
                ('autoBlock', models.BooleanField(default=False)),
            ],
            bases=('todolist.mydb',),
        ),
        migrations.AddField(
            model_name='todoitemdb',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.userdb'),
        ),
        migrations.AddField(
            model_name='authenticationtokendb',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.userdb'),
        ),
    ]