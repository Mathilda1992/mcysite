# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-02 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0034_auto_20170302_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='stop_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]