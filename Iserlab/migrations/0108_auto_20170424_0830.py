# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-24 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0107_auto_20170424_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vminstance',
            name='vncurl',
            field=models.URLField(blank=True, null=True),
        ),
    ]
