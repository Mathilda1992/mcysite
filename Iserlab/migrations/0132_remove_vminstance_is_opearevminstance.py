# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-17 05:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0131_auto_20170517_0549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vminstance',
            name='is_opeareVMInstance',
        ),
    ]
