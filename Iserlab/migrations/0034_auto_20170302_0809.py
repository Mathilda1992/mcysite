# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-02 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Iserlab', '0033_auto_20170302_0804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='stu_username',
            new_name='stu',
        ),
        migrations.RenameField(
            model_name='delivery',
            old_name='teacher_username',
            new_name='teacher',
        ),
        migrations.AddField(
            model_name='delivery',
            name='desc',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='name',
            field=models.CharField(default='delivery_record', max_length=100),
        ),
        migrations.AlterField(
            model_name='expinstance',
            name='description',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
