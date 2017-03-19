# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-19 08:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0087_auto_20170319_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatetime', models.DateTimeField(auto_now=True, null=True)),
                ('network_instance_id', models.CharField(blank=True, max_length=50, null=True)),
                ('subnet_instance_id', models.CharField(blank=True, max_length=50, null=True)),
                ('tenant_id', models.CharField(blank=True, max_length=50, null=True)),
                ('exp_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Iserlab.Score')),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Iserlab.Network')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Iserlab.User')),
            ],
            options={
                'ordering': ['-createtime'],
            },
        ),
    ]
