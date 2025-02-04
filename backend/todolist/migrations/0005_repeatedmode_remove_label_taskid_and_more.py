# Generated by Django 5.1 on 2024-11-11 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_taskcontainer_task_createddate_task_isdonestate_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepeatedMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('startDuration', models.DateField(verbose_name='Start of Repeat')),
                ('endDuration', models.DateField(verbose_name='End of Repeat')),
            ],
        ),
        migrations.RemoveField(
            model_name='label',
            name='taskID',
        ),
        migrations.RemoveField(
            model_name='task',
            name='repeatEveryDay',
        ),
        migrations.RemoveField(
            model_name='task',
            name='repeatEveryWeek',
        ),
        migrations.RemoveField(
            model_name='task',
            name='repeatOne',
        ),
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(to='todolist.label'),
        ),
        migrations.AddField(
            model_name='taskcontainer',
            name='tasksList',
            field=models.ManyToManyField(to='todolist.task'),
        ),
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('containerList', models.ManyToManyField(to='todolist.taskcontainer')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='repeatModeList',
            field=models.ManyToManyField(to='todolist.repeatedmode'),
        ),
        migrations.DeleteModel(
            name='TaskRelation',
        ),
    ]
