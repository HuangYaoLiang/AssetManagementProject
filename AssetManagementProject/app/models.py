"""
实体类
黄耀樑 2016-07-20
"""

import json
#import django.utils.timezone as timezone

from django.db import models
#from django.db import connection
from app.dbtools import dbhelp,dbbase
from datetime import *

#import datetime



# Create your models here.


# 职员信息
# 黄耀樑 2016-07-08
class PersonInfo(dbbase):
    
    name = models.CharField(u'姓名',max_length=10, default='')
    position = models.CharField(u'所在位置',max_length=50, default='')
    contact = models.CharField(u'联系方式',max_length=50, default='')
    remark = models.TextField(u'备注', default='',blank=True)

    #def getDropDownList(self):
    #    return tuple([(0,'无')] + list(PersonInfo.objects.values_list('id','name').order_by('name')))

    ## 获取实体  职员信息
    ## 黄耀樑 2016-07-26
    #def getOne(self, id=0):
    #    sql = '''
    #    SELECT t1.*
    #    FROM app_personinfo AS t1
    #    WHERE t1.id=%s
    #    '''
    #    return dbhelp.querySingle(sql, [id])

    ## 获取列表  职员信息
    ## 黄耀樑 2016-07-26
    #def getList(self, where='1=1', sort='id', order=''):
    #    #sqlWhere = "1=1" # t1.category='台式机'
    #    sql = '''
    #    SELECT t1.*
    #    FROM app_personinfo AS t1
    #    WHERE %s
    #    ORDER BY %s %s 
    #    ''' % (where, sort, order)
    #    return dbhelp.queryList(sql)


# 资产信息
class AssetInfo(dbbase):
    person_id = models.IntegerField(u'使用者ID', default=0)
    position = models.CharField(u'存放地点',max_length=50, default='')
    serial_number = models.CharField(u'资产编号',max_length=20, default='')
    name = models.CharField(u'资产名称',max_length=100, default='')
    category = models.CharField(u'资产分类',max_length=10, default='')
    quantity = models.IntegerField(u'资产数量',default=1)
    unit_price = models.IntegerField(u'单价',default=0)
    total_price = models.IntegerField(u'总价值',default=0)
    fiscal_funds = models.IntegerField(u'财政性资金',default=0)
    use_department = models.CharField(u'使用部门',max_length=50, default='')
    fund_source = models.CharField(u'资金来源',max_length=50, default='', blank=True)
    get_time = models.DateField(u'取得时间',null=True, blank=True)
    remark = models.TextField(u'备注', default='',blank=True)
    state = models.CharField(u'状态',max_length=10, default='')


# 硬件信息
class HardwareInfo(dbbase):    
    asset_id = models.IntegerField(u'资产ID', default=0)
    system_os = models.CharField(u'操作系统',max_length=100, default='')
    pc_score = models.IntegerField(u'鲁大师评分', default=0)
    pc_cpu = models.CharField(u'CPU',max_length=50, default='')
    pc_memory = models.CharField(u'内存',max_length=50, default='')
    pc_mac = models.CharField(u'MAC',max_length=20, default='')
    pc_ip = models.CharField(u'IP4',max_length=20, default='')
    pc_description = models.TextField(u'PC详细描述', default='', blank=True)

    # 获取实体  硬件信息
    # 黄耀樑 2016-07-08
    def getOne(self, id=0):
        sql = '''
        SELECT t1.*,t2.name AS person_name,t3.system_os,t3.pc_score,t3.pc_cpu,t3.pc_memory,t3.pc_mac,t3.pc_ip,t3.pc_description
        FROM app_assetinfo AS t1
        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id
        LEFT JOIN app_HardwareInfo AS t3 ON t1.id=t3.asset_id
        WHERE t1.id=%s
        '''
        return dbhelp.querySingle(sql, [id])

    # 获取列表  硬件信息
    # 黄耀樑 2016-07-08
    def getList(self, where='1=1', sort='id', order=''):
        where = "t1.category='台式机'"
        sql = '''
        SELECT t1.*,t2.name AS person_name,t3.system_os,t3.pc_score,t3.pc_cpu,t3.pc_memory,t3.pc_mac,t3.pc_ip,t3.pc_description
        FROM app_assetinfo AS t1
        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id
        LEFT JOIN app_HardwareInfo AS t3 ON t1.id=t3.asset_id
        WHERE %s
        ORDER BY %s %s 
        ''' % (where, sort, order)
        return dbhelp.queryList(sql)

    # 获取硬件信息列表最大编号
    # 黄耀樑 2016-07-08
    def getMaxNumber(self):
        sql = '''
        SELECT MAX(serial_number)
        FROM app_assetinfo
        WHERE category='台式机' AND serial_number+0=serial_number
        '''
        return dbhelp.queryScalar(sql)
        

## 打印机信息
#class PrinterInfo(models.Model):
#    asset_id = models.IntegerField(u'资产ID', default=0)
#    person_id = models.IntegerField(u'使用者ID', default=0)

#    #serial_number = models.CharField(u'编号',max_length=20, default='')
#    #position = models.CharField(u'所在位置',max_length=50, default='')
#    #prt_model = models.CharField(u'打印机型号',max_length=50, default='')
#    #use_time = models.DateTimeField(u'入库时间',null=True, blank=True)
#    #prt_description = models.TextField(u'打印机详细描述', default='',blank=True)
#    #remark = models.TextField(u'备注', default='',blank=True)
#    #price = models.IntegerField(u'价值',default=0)

#    # 获取打印机信息列表
#    def getPrinterList(self,id=0):
#        sqlWhere = '1=1'
#        if not id :
#            sqlWhere = 't1.person_id>0'
#        else:
#            id = int(id)
#            if id == -20:
#                sqlWhere = 't1.person_id>0'
#            elif id == -30:
#                sqlWhere = 't1.person_id=0'
#        cursor = connection.cursor()
#        cursor.execute("""
#        SELECT t1.*,t2.name AS person_name,t3.*
#        FROM app_PrinterInfo AS t1
#        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id
#        LEFT JOIN app_assetinfo AS t3 ON t1.asset_id=t3.id
#        WHERE %s
#        ORDER BY position""" % (sqlWhere))
#        index = cursor.description
#        result = []
#        for row in cursor.fetchall():
#            obj = {}
#            for i in range(len(index)):
#                obj[index[i][0]] = row[i]
#            result.append(obj)
#        cursor.close()
#        connection.close()
#        return result

#    # 获取打印机信息列表最大编号
#    # 黄耀樑 2016-07-08
#    def getMaxNumber(self):
#        cursor = connection.cursor()
#        sql = '''SELECT MAX(serial_number)
#        FROM app_PrinterInfo
#        WHERE serial_number+0=serial_number'''
#        cursor.execute(sql)                
#        obj = cursor.fetchone()[0]
#        return obj


# 变更记录
class ChangeInfo(dbbase):
    serial_number = models.CharField(u'编号',max_length=20, default='')
    position = models.CharField(u'所在位置',max_length=50, default='')
    name = models.CharField(u'姓名',max_length=10, default='')
    type = models.CharField(u'变更类型',max_length=10, default='')
    remark = models.TextField(u'变更说明', default='')
    create_time = models.DateField(u'创建时间', default=date.today())
    state = models.IntegerField(u'状态',default=0) # 0:待处理 1:已处理 -1:不处理

    ## 获取实体  变更记录
    ## 黄耀樑 2016-07-26
    #def getOne(self, id=0):
    #    sql = '''
    #    SELECT t1.*
    #    FROM app_changeinfo AS t1
    #    WHERE t1.id=%s
    #    '''
    #    return dbhelp.querySingle(sql, [id])

    ## 获取列表  变更记录
    ## 黄耀樑 2016-07-28
    #def getList(self, where='1=1', sort='id', order=''):
    #    sql = '''
    #    SELECT t1.*
    #    FROM app_changeinfo AS t1
    #    WHERE %s
    #    ORDER BY %s %s
    #    ''' % (where, sort, order)
    #    return dbhelp.queryList(sql)


# 点赞图片
class LikeImageInfo(models.Model):
    pc_ip = models.CharField(u'IP4',max_length=20, default='')
    img_number = models.IntegerField(u'图片编号',default=0)