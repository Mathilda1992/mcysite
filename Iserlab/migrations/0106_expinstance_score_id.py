# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-23 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0105_auto_20170423_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='expinstance',
            name='score_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
