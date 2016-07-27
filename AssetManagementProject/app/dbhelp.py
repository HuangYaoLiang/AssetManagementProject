"""
数据库工具类
黄耀樑 2016-07-20
"""

from django.db import connection

import json
import datetime

class dbhelp():

    # 设置值，用于格式化
    # 黄耀樑 2016-07-27
    def __setValue(val):
        if isinstance(val, datetime.datetime):
            val = val.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(val, datetime.date):
            val = val.strftime('%Y-%m-%d')
        return val

    # 获取实体
    # 黄耀樑 2016-07-26
    def querySingle(sql, params=[]):
        cursor = connection.cursor()
        cursor.execute(sql, params)
        column = cursor.description # 获取所有列名
        obj = {}
        row = cursor.fetchone()
        for i in range(len(column)):
            obj[column[i][0]] = dbhelp.__setValue(row[i])
        return obj

    # 获取列表
    # 黄耀樑 2016-07-26
    def queryList(sql, sort='id', order=''):
        cursor = connection.cursor()
        cursor.execute(sql)
        column = cursor.description # 获取所有列名
        result = []
        for row in cursor.fetchall():
            obj = {}
            for i in range(len(column)):
                obj[column[i][0]] = dbhelp.__setValue(row[i])
            result.append(obj)
        cursor.close()
        connection.close()
        return result

    # 获取单列
    # 黄耀樑 2016-07-26
    def queryScalar(sql):
        cursor = connection.cursor() 
        cursor.execute(sql)                
        val = ''
        query = cursor.fetchone()
        if len(query) > 0:
            val = query[0]
        return val
