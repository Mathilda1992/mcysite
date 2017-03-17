# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-14 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0069_score_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='group',
        ),
        migrations.AddField(
            model_name='score',
            name='group_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]