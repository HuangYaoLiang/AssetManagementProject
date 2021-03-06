﻿"""
数据库工具类
黄耀樑 2016-07-20
"""

import json
import datetime

from django.db import models
from django.db import connection
from app.utils import utils

# 数据库操作类
# 黄耀樑 2016-07-26
class dbhelp():

    # 获取实体
    # 黄耀樑 2016-07-26
    def querySingle(sql, params=[]):
        cursor = connection.cursor()
        cursor.execute(sql, params)
        column = cursor.description # 获取所有列名
        obj = {}
        row = cursor.fetchone()
        for i in range(len(column)):
            obj[column[i][0]] = utils.formatValue(row[i])
        return obj

    # 获取列表
    # 黄耀樑 2016-07-26
    def queryList(sql, params=[]):
        cursor = connection.cursor()
        cursor.execute(sql, params)
        column = cursor.description # 获取所有列名
        result = []
        for row in cursor.fetchall():
            obj = {}
            for i in range(len(column)):
                obj[column[i][0]] = utils.formatValue(row[i])
            result.append(obj)
        cursor.close()
        connection.close()
        return result

    # 获取单列
    # 黄耀樑 2016-07-26
    def queryScalar(sql, params=[]):
        cursor = connection.cursor() 
        cursor.execute(sql, params)                
        val = ''
        query = cursor.fetchone()
        if len(query) > 0:
            val = query[0]
        return val

    # 获取下拉列表
    # 黄耀樑 2016-07-29
    def queryDropDownList(sql, params=[]):
        cursor = connection.cursor()
        cursor.execute(sql, params)
        column = cursor.description # 获取所有列名
        result = []
        for row in cursor.fetchall():
            list = []
            for i in range(len(column)):
                list.append(utils.formatValue(row[i]))
            result.append(tuple(list))
        cursor.close()
        connection.close()
        return result


# 数据库父类
# 黄耀樑 2016-07-26
class dbbase():
    
    # 获取实体
    # 黄耀樑 2016-07-26
    def getOne(self, id):
        # 因为要使用参数化操作数据库，只能拼接sql语句
        sql = '''
        SELECT *
        FROM ''' + self._meta.db_table + '''
        WHERE id=%s
        '''
        return dbhelp.querySingle(sql, [id])

    # 获取列表
    # 黄耀樑 2016-07-26
    def getList(self, where=None, sort=None, order=None, params=[]):
        if not where:
            where = '1=1'
        if not sort:
            sort = 'id'
        if not order:
            order = ''
        # 因为要使用参数化操作数据库，只能拼接sql语句
        sql = '''
        SELECT *
        FROM ''' + self._meta.db_table + '''
        WHERE ''' + where + '''
        ORDER BY ''' + sort + ''' ''' + order + ''' 
        '''
        return dbhelp.queryList(sql, params)

    def getDropDownList(self,text='name', value='id', sort='name'):
        #query = self._meta.model.objects.values_list('id','name').order_by('name')
        #list = tuple([(0,'无')] + list(query))
        #return list
        sql = '''
        SELECT %s,%s
        FROM %s
        ORDER BY %s
        ''' % (value, text, self._meta.db_table, sort)
        query = dbhelp.queryDropDownList(sql)
        list = tuple([(0,'无')] + query)
        return list

