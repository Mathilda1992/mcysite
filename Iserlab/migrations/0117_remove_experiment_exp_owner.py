# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-25 00:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0116_remove_vmimage_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='exp_owner',
        ),
    ]
