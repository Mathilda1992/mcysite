# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-14 06:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_blog_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
    ]
