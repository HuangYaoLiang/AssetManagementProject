"""
Definition of models.
"""

from django.db import models
from django.db import connection

import datetime

# Create your models here.

# 职员信息
class PersonInfo(models.Model):
    name = models.CharField(u'姓名',max_length=10, default='')
    position = models.CharField(u'所在位置',max_length=50, default='')
    contact = models.CharField(u'联系方式',max_length=50, default='')

    def getPersonDropDownList(self):
        return tuple([(0,'无')] + list(PersonInfo.objects.values_list('id','name').order_by('name')))

# 硬件信息
class HardwareInfo(models.Model):
    serial_number = models.CharField(u'编号',max_length=20, default='')
    person_id = models.IntegerField(u'使用者ID')
    position = models.CharField(u'所在位置',max_length=50, default='')
    system_os = models.CharField(u'操作系统',max_length=100, default='')
    pc_score = models.IntegerField(u'鲁大师评分',default=0)
    pc_cpu = models.CharField(u'CPU',max_length=50, default='')
    pc_memory = models.CharField(u'内存',max_length=50, default='')
    pc_mac = models.CharField(u'MAC',max_length=20, default='')
    pc_ip = models.CharField(u'IP4',max_length=20, default='')
    use_time = models.DateTimeField(u'启用时间',null=True, blank=True)
    pc_description = models.TextField(u'PC详细描述', default='',blank=True)

    # 获取硬件信息列表
    # 黄耀樑 2016-07-08
    def getHardwareList(self,id=0,sort='', order=''):
        sqlWhere = '1=1'
        if not id :
            sqlWhere = 't1.person_id>0'
        else:
            id = int(id)
            if id == -20:
                sqlWhere = 't1.person_id>0'
            elif id == -30:
                sqlWhere = 't1.person_id=0'
        cursor = connection.cursor()
        sql = '''SELECT t1.id,t1.serial_number,t1.position,t1.system_os,t1.pc_score,t1.pc_cpu,t1.pc_memory,t1.use_time,t2.name AS person_name,t1.pc_mac,t1.pc_ip,t1.pc_description
        FROM app_HardwareInfo AS t1
        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id
        WHERE %s
        ORDER BY t1.%s %s''' % (sqlWhere, sort, order)
        cursor.execute(sql)                
        list = []
        for row in cursor.fetchall():
            dic = {}
            dic['id'] = row[0]
            dic['serial_number'] = row[1]
            dic['position'] = row[2]
            dic['system_os'] = row[3]
            dic['pc_score'] = row[4]
            dic['pc_cpu'] = row[5]
            dic['pc_memory'] = row[6]
            dic['use_time'] = row[7]
            dic['person_name'] = row[8]
            dic['pc_mac'] = row[9]
            dic['pc_ip'] = row[10]
            dic['pc_description'] = row[11]
            list.append(dic)
        return list

    # 获取硬件信息列表最大编号
    # 黄耀樑 2016-07-08
    def getMaxNumber(self):
        cursor = connection.cursor()
        sql = '''SELECT MAX(serial_number)
        FROM app_HardwareInfo
        WHERE serial_number+0=serial_number'''
        cursor.execute(sql)                
        obj = cursor.fetchone()[0]
        return obj

# 打印机信息
class PrinterInfo(models.Model):
    serial_number = models.CharField(u'编号',max_length=20, default='')
    person_id = models.IntegerField(u'使用者ID')
    position = models.CharField(u'所在位置',max_length=50, default='')
    prt_model = models.CharField(u'打印机型号',max_length=50, default='')
    use_time = models.DateTimeField(u'启用时间',null=True, blank=True)
    prt_description = models.TextField(u'打印机详细描述', default='',blank=True)

    # 获取打印机信息列表
    def getPrinterList(self,id=0):
        sqlWhere = '1=1'
        if not id :
            sqlWhere = 't1.person_id>0'
        else:
            id = int(id)
            if id == -20:
                sqlWhere = 't1.person_id>0'
            elif id == -30:
                sqlWhere = 't1.person_id=0'
        cursor = connection.cursor()
        cursor.execute("""
        SELECT t1.id,t1.serial_number,t1.position,t1.prt_model,t1.prt_description,t2.name AS person_name
        FROM app_PrinterInfo AS t1
        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id
        WHERE %s
        ORDER BY t1.position""" % (sqlWhere))
        list = []
        for row in cursor.fetchall():
            dic = {}
            dic['id'] = row[0]
            dic['serial_number'] = row[1]
            dic['position'] = row[2]
            dic['prt_model'] = row[3]
            dic['prt_description'] = row[4]
            dic['person_name'] = row[5]
            list.append(dic)
        return list

    # 获取打印机信息列表最大编号
    # 黄耀樑 2016-07-08
    def getMaxNumber(self):
        cursor = connection.cursor()
        sql = '''SELECT MAX(serial_number)
        FROM app_PrinterInfo
        WHERE serial_number+0=serial_number'''
        cursor.execute(sql)                
        obj = cursor.fetchone()[0]
        return obj

# 变更记录
class ChangeLog(models.Model):
    name = models.CharField(u'姓名',max_length=10, default='')
    type = models.CharField(u'变更类型',max_length=10, default='')
    remark = models.TextField(u'变更说明', default='')
    create_time = models.DateTimeField(u'创建时间', default=datetime.datetime.now())

# 点赞图片
class LikeImageInfo(models.Model):
    pc_ip = models.CharField(u'IP4',max_length=20, default='')
    img_number = models.IntegerField(u'图片编号',default=0)

