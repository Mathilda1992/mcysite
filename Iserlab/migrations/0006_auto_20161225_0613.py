# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-25 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0005_auto_20161225_0535'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='network',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['stu_username']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
        migrations.AlterModelOptions(
            name='vmimage',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='exp_id',
        ),
        migrations.AddField(
            model_name='network',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='network',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
