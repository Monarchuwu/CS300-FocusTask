# Generated by Django 5.1 on 2024-11-06 18:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_alter_task_repeateveryday_alter_task_repeateveryweek_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date')),
                ('containerName', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='createdDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created date'),
        ),
        migrations.AddField(
            model_name='task',
            name='isDoneState',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachFile', models.FileField(upload_to='')),
                ('taskID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.task')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('taskID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.task')),
                ('taskContainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.taskcontainer')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSubrelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mainTask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Main_task', to='todolist.task')),
                ('subTask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sub_task', to='todolist.task')),
            ],
        ),
        migrations.CreateModel(
            name='URLAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachFile', models.URLField()),
                ('taskID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.task')),
            ],
        ),
    ]
