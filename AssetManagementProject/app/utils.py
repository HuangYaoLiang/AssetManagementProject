"""
常用工具类
黄耀樑 2016-07-20
"""

import datetime
import re

from django.http import HttpRequest
# {"total":28,"rows":[{"productid":"FI-SW-01","productname":"Koi","unitcost":10.00,"status":"P","listprice":36.50,"attr1":"Large","itemid":"EST-1"}]}



class utils():

    # 获取 snowui-datagrid json格式数据源
    # 黄耀樑 2016-07-22
    def getDatagrid(query=[], total=0):
        if not total:
            total = len(query)
        return {"total": total, "rows": query}

    # 封装表单数据到实体
    # 黄耀樑 2016-07-26
    def createObject(model, request, exclude=[]):
        for x in request.POST:
            if x in model._meta.get_all_field_names() and x != 'id':
                if not exclude or (len(exclude) > 0 and not x in exclude):
                    #val = getattr(model, x)
                    #p = re.compile(r'_time$') # 时间属性 一定要_time 这个结尾 要不然无法动态判断
                    #new_val = request.POST[x]
                    #if p.search(x):
                    #    if new_val:
                    #        setattr(model, x, new_val)
                    #else:
                    #    setattr(model, x, new_val)
                    new_val = request.POST[x]
                    if new_val:
                        setattr(model, x, new_val)

    # 设置值，用于格式化，私有函数
    # 黄耀樑 2016-07-27
    def formatValue(val):
        if isinstance(val, datetime.datetime):
            val = val.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(val, datetime.date):
            val = val.strftime('%Y-%m-%d')
        val = val if val != None else ''
        return val

    # 实体数据序列化JSON对象
    # 黄耀樑 2016-07-28
    def toJsonObject(obj):
        #fields = []
        #for field in obj._meta.fields:
        #    fields.append(field.name)    
        #d = {}
        #v = ''
        #for attr in fields:
        #    d[attr] = utils.formatValue(getattr(obj, attr))

        d = {}
        v = ''
        exclude = ['_state', 'dbbase_ptr_id'] # 排除的属性        
        for attr in obj.__dict__:
            if attr not in exclude:
                v = getattr(obj, attr)
                d[attr] = utils.formatValue(v)
        return d

    # 反射实体
    # 黄耀樑 2016-07-28
    def importModel(key):
        # models 比较特殊 需要这种形式
        m = __import__("app.models",{},{},["models"])  
        p = re.compile(r'^' + key + 'info$', re.I)
        o = {}
        for k in m.__dict__:
            if p.match(k):
                o = getattr(m, k)
        return o

