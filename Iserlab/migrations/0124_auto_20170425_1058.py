# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-25 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0123_auto_20170425_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vm',
            name='exp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Iserlab.Experiment'),
        ),
        migrations.AlterField(
            model_name='vmimage',
            name='is_public',
            field=models.CharField(default='private', max_length=10),
        ),
        migrations.AlterField(
            model_name='vmimage',
            name='min_disk',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='vmimage',
            name='min_ram',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='vmimage',
            name='size',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
