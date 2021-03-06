# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.IntegerField(default=0, verbose_name='使用者ID')),
                ('position', models.CharField(default='', max_length=50, verbose_name='存放地点')),
                ('serial_number', models.CharField(default='', max_length=20, verbose_name='资产编号')),
                ('name', models.CharField(default='', max_length=100, verbose_name='资产名称')),
                ('category', models.CharField(default='', max_length=10, verbose_name='资产分类')),
                ('quantity', models.IntegerField(default=1, verbose_name='资产数量')),
                ('unit_price', models.IntegerField(default=0, verbose_name='单价')),
                ('total_price', models.IntegerField(default=0, verbose_name='总价值')),
                ('fiscal_funds', models.IntegerField(default=0, verbose_name='财政性资金')),
                ('use_department', models.CharField(default='', max_length=50, verbose_name='使用部门')),
                ('fund_source', models.CharField(blank=True, default='', max_length=50, verbose_name='资金来源')),
                ('get_time', models.DateField(blank=True, null=True, verbose_name='取得时间')),
                ('remark', models.TextField(blank=True, default='', verbose_name='备注')),
                ('state', models.CharField(default='', max_length=10, verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(default='', max_length=20, verbose_name='编号')),
                ('name', models.CharField(default='', max_length=10, verbose_name='姓名')),
                ('type', models.CharField(default='', max_length=10, verbose_name='变更类型')),
                ('remark', models.TextField(default='', verbose_name='变更说明')),
                ('create_time', models.DateField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('state', models.IntegerField(default=0, verbose_name='状态')),
            ],
        ),
        migrations.CreateModel(
            name='HardwareInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.IntegerField(default=0, verbose_name='资产ID')),
                ('system_os', models.CharField(default='', max_length=100, verbose_name='操作系统')),
                ('pc_score', models.IntegerField(default=0, verbose_name='鲁大师评分')),
                ('pc_cpu', models.CharField(default='', max_length=50, verbose_name='CPU')),
                ('pc_memory', models.CharField(default='', max_length=50, verbose_name='内存')),
                ('pc_mac', models.CharField(default='', max_length=20, verbose_name='MAC')),
                ('pc_ip', models.CharField(default='', max_length=20, verbose_name='IP4')),
                ('pc_description', models.TextField(blank=True, default='', verbose_name='PC详细描述')),
            ],
        ),
        migrations.CreateModel(
            name='LikeImageInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pc_ip', models.CharField(default='', max_length=20, verbose_name='IP4')),
                ('img_number', models.IntegerField(default=0, verbose_name='图片编号')),
            ],
        ),
        migrations.CreateModel(
            name='PersonInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10, verbose_name='姓名')),
                ('position', models.CharField(default='', max_length=50, verbose_name='所在位置')),
                ('contact', models.CharField(default='', max_length=50, verbose_name='联系方式')),
                ('remark', models.TextField(blank=True, default='', verbose_name='备注')),
            ],
        ),
    ]
