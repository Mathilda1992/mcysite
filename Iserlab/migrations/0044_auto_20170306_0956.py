# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-06 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0043_score_socre_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
