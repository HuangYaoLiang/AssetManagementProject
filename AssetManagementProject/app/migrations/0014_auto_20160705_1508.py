# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 07:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20160705_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personinfo',
            name='pc_ip',
        ),
        migrations.RemoveField(
            model_name='personinfo',
            name='pc_mac',
        ),
        migrations.AlterField(
            model_name='changelog',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 5, 15, 8, 4, 817656), verbose_name='创建时间'),
        ),
    ]
