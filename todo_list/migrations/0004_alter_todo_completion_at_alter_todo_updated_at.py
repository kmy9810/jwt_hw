# Generated by Django 4.2 on 2023-04-24 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0003_alter_todo_completion_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='completion_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 24, 17, 6, 38, 973817), null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 24, 17, 6, 38, 973740), null=True),
        ),
    ]