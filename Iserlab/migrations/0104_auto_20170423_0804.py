# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-23 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0103_auto_20170423_0612'),
    ]

    operations = [
        migrations.AddField(
            model_name='routerinstance',
            name='gateway_ip_address',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='routerinstance',
            name='gateway_net_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='routerinstance',
            name='gateway_subnet_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
