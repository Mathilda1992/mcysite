# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-08 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0054_score_delivery_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='startTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
