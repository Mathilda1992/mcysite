# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-25 00:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0117_remove_experiment_exp_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment',
            old_name='owner_name',
            new_name='exp_owner_name',
        ),
    ]