# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 11:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160630_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelog',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 30, 19, 25, 33, 360207), verbose_name='创建时间'),
        ),
    ]
