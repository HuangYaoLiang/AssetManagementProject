"""
Definition of models.
"""

from django.db import models

# Create your models here.

# 职员信息
class PersonInfo(models.Model):
    name = models.CharField(help_text='姓名',max_length=10, default='')
    position = models.CharField(help_text='所在位置',max_length=50, default='')
    contact = models.CharField(help_text='联系方式',max_length=50, default='')
    pc_mac = models.CharField(help_text='MAC',max_length=20, default='')
    pc_ip = models.CharField(help_text='IP4',max_length=20, default='')

# 硬件信息
class HardwareInfo(models.Model):
    serial_number = models.CharField(help_text='编号',max_length=10, default='')
    person_id = models.IntegerField(help_text='使用者ID')
    position = models.CharField(help_text='所在位置',max_length=50, default='')
    system_os = models.CharField(help_text='操作系统',max_length=20, default='')
    pc_score = models.IntegerField(help_text='鲁大师评分',default=0)
    pc_cpu = models.CharField(help_text='CPU',max_length=50, default='')
    pc_memory = models.CharField(help_text='CPU',max_length=50, default='')
    pc_description = models.TextField(help_text='PC详细描述', default='')
    use_time = models.DateTimeField(help_text='启用时间',null=True, blank=True)

# 打印机信息
class PrinterInfo(models.Model):
    serial_number = models.CharField(help_text='编号',max_length=10, default='')
    person_id = models.IntegerField(help_text='使用者ID')
    position = models.CharField(help_text='所在位置',max_length=50, default='')
    prt_model = models.CharField(help_text='打印机型号',max_length=50, default='')
    prt_description = models.TextField(help_text='打印机详细描述', default='')
    use_time = models.DateTimeField(help_text='启用时间',null=True, blank=True)

# 变更记录
class ChangeLog(models.Model):
    serial_number = models.CharField(help_text='编号',max_length=10, default='')
    name = models.CharField(help_text='姓名',max_length=10, default='')
    type = models.CharField(help_text='变更类型',max_length=10, default='')
    remark = models.TextField(help_text='变更说明', default='')
    create_time = models.DateTimeField(help_text='创建时间', auto_now=True)

