# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-21 06:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0096_portinstance_routerinstance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portinstance',
            options={'ordering': ['-createtime']},
        ),
        migrations.AlterModelOptions(
            name='routerinstance',
            options={'ordering': ['-createtime']},
        ),
    ]
