# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-14 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='type',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
