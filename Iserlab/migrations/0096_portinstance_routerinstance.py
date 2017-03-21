# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-21 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0095_auto_20170320_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_username', models.CharField(max_length=50)),
                ('portInstance_id', models.CharField(max_length=50)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(max_length=20)),
                ('device_owner', models.CharField(max_length=50)),
                ('device_id', models.CharField(max_length=50)),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True, null=True)),
                ('network_id', models.CharField(max_length=50)),
                ('subnet_id', models.CharField(max_length=50)),
                ('ip_address', models.CharField(max_length=20)),
                ('tenant_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RouterInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_username', models.CharField(max_length=50)),
                ('routerIntance_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=20)),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True, null=True)),
                ('gateway_net_id', models.CharField(max_length=50)),
                ('gateway_subnet_id', models.CharField(max_length=50)),
                ('gateway_ip_address', models.CharField(max_length=20)),
                ('tenant_id', models.CharField(max_length=50)),
            ],
        ),
    ]
