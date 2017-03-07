# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-07 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0048_auto_20170307_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='shared_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='is_shared',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='network',
            name='shared_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='finishedTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='score_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='vmimage',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='vmimage',
            name='is_shared',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vmimage',
            name='shared_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='vminstance',
            name='updatetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
