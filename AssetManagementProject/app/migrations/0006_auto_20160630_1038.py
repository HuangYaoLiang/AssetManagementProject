# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 02:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_likeimageinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelog',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 30, 10, 38, 49, 116707), help_text='创建时间'),
        ),
    ]
