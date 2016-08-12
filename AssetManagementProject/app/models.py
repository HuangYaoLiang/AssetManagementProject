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

# 点赞图片
class LikeImageInfo(models.Model):
    pc_ip = models.CharField(u'IP4',max_length=20, default='')
    img_number = models.IntegerField(u'图片编号',default=0)

# 职员信息
# 黄耀樑 2016-07-08
class PersonInfo(models.Model, dbbase):    
    name = models.CharField(u'姓名',max_length=10, default='')
    position = models.CharField(u'所在位置',max_length=50, default='')
    contact = models.CharField(u'联系方式',max_length=50, default='')
    remark = models.TextField(u'备注', default='',blank=True)


# 资产信息
class AssetInfo(models.Model, dbbase):
    person_id = models.IntegerField(u'使用者ID', default=0)
    position = models.CharField(u'存放地点',max_length=50, default='')
    serial_number = models.CharField(u'资产编号',max_length=20, default='')
    name = models.CharField(u'资产名称',max_length=100, default='')
    category = models.CharField(u'资产分类',max_length=10, default='')
    quantity = models.IntegerField(u'资产数量',default=1)
    unit_price = models.IntegerField(u'单价',default=0)
    total_price = models.IntegerField(u'总价值',default=0)
    fiscal_funds = models.IntegerField(u'财政性资金',default=0)
    use_department = models.CharField(u'使用部门',max_length=50, default='人事代理部')
    fund_source = models.CharField(u'资金来源',max_length=50, default='人才办', blank=True)
    get_time = models.DateField(u'取得时间',null=True, blank=True)
    remark = models.TextField(u'备注', default='',blank=True)
    state = models.CharField(u'状态',max_length=10, default='OK')

    # 获取实体  资产信息
    # 黄耀樑 2016-07-08
    def getOne(self, id):
        sql = '''
        SELECT t1.*,t2.name AS person_name
        FROM app_assetinfo AS t1
        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id
        WHERE t1.id=%s
        '''
        return dbhelp.querySingle(sql, [id])

    # 获取列表  资产信息
    # 黄耀樑 2016-07-08
    def getList(self, where=None, sort=None, order=None):
        if not where:
            where = '1=1'
        if not sort:
            sort = 'id'
        if not order:
            order = ''
        sql = '''
        SELECT * FROM (
        SELECT t1.*,t2.name AS person_name
        FROM app_assetinfo AS t1
        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id)
        WHERE %s
        ORDER BY %s %s 
        ''' % (where, sort, order)
        return dbhelp.queryList(sql)

    # 获取最大编号 资产信息
    # 黄耀樑 2016-07-08
    def getMaxNumber(self, where=None):
        if not where:
            where = '1=1'
        sql = '''
        SELECT COUNT(id)+1
        FROM app_assetinfo
        WHERE %s
        ''' % (where)
        return dbhelp.queryScalar(sql)


# 硬件信息
class HardwareInfo(models.Model, dbbase):    
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
    def getOne(self, id):
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
    def getList(self, where=None, sort=None, order=None):
        if not where:
            where = ''
        if not sort:
            sort = 'id'
        if not order:
            order = ''
        sqlWhere = "1=1"
        if where:
            sqlWhere += (" AND " + where)
        sql = '''
        SELECT * FROM (
        SELECT t1.*,t2.name AS person_name,t3.system_os,t3.pc_score,t3.pc_cpu,t3.pc_memory,t3.pc_mac,t3.pc_ip,t3.pc_description
        FROM app_assetinfo AS t1
        LEFT JOIN app_PersonInfo AS t2 ON t1.person_id=t2.id
        LEFT JOIN app_HardwareInfo AS t3 ON t1.id=t3.asset_id)
        WHERE %s
        ORDER BY %s %s 
        ''' % (sqlWhere, sort, order)
        return dbhelp.queryList(sql)

    # 获取最大编号 硬件信息
    # 黄耀樑 2016-07-08
    def getMaxNumber(self,where=None):
        if not where:
            where = '1=1'
        sql = '''
        SELECT COUNT(id)+1
        FROM app_assetinfo
        WHERE %s
        ''' % (where)
        return dbhelp.queryScalar(sql)

    # 获取列表  台式机
    # 黄耀樑 2016-07-08
    def getDesktopList(self, where=None, sort=None, order=None):
        if not where:
            where = ''
        if not sort:
            sort = 'id'
        if not order:
            order = ''
        sqlWhere = "category='台式机'"
        if where:
            sqlWhere += (" AND " + where)
        return self.getList(sqlWhere, sort, order);

    # 获取列表  服务器
    # 黄耀樑 2016-07-08
    def getServerList(self, where=None, sort=None, order=None):
        if not where:
            where = ''
        if not sort:
            sort = 'id'
        if not order:
            order = ''
        sqlWhere = "category='PC服务器'"
        if where:
            sqlWhere += (" AND " + where)
        return self.getList(sqlWhere, sort, order);

    # 获取列表  笔记本
    # 黄耀樑 2016-07-08
    def getNotebookList(self, where=None, sort=None, order=None):
        if not where:
            where = ''
        if not sort:
            sort = 'id'
        if not order:
            order = ''
        sqlWhere = "category='笔记本电脑'"
        if where:
            sqlWhere += (" AND " + where)
        return self.getList(sqlWhere, sort, order);

# 变更记录
class ChangeInfo(models.Model, dbbase):
    serial_number = models.CharField(u'编号',max_length=20, default='')
    position = models.CharField(u'所在位置',max_length=50, default='')
    name = models.CharField(u'姓名',max_length=10, default='')
    type = models.CharField(u'变更类型',max_length=10, default='')
    remark = models.TextField(u'变更说明', default='')
    create_time = models.DateField(u'创建时间', default=date.today())
    state = models.IntegerField(u'状态',default=0) # 0:待处理 1:已处理 -1:不处理
    process_time = models.DateField(u'处理时间',null=True, blank=True)


# 退回记录
class UntreadInfo(models.Model, dbbase):
    untread_time = models.DateField(u'退回时间', default=date.today())
    remark = models.TextField(u'备注', default='',blank=True)


# 退回明细
class UntreadDetailInfo(models.Model, dbbase):
    untread_id = models.IntegerField(u'退回ID', default=0)
    category = models.CharField(u'资产类型',max_length=10, default='')
    serial_number = models.CharField(u'资产编号',max_length=20, default='')
    name = models.CharField(u'资产名称',max_length=100, default='')
    reason = models.CharField(u'报废原因',max_length=50, default='')
    remark = models.TextField(u'备注', default='',blank=True)


# 仓库信息
class WarehouseInfo(models.Model, dbbase):
    category = models.CharField(u'资产类型',max_length=10, default='')
    name = models.CharField(u'资产名称',max_length=100, default='')
    position = models.CharField(u'存放地点',max_length=50, default='')
    quantity = models.IntegerField(u'资产数量',default=1)
    state = models.CharField(u'状态',max_length=10, default='')
    remark = models.TextField(u'备注', default='',blank=True)