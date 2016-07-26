"""
常用工具类
黄耀樑 2016-07-20
"""

from django.http import HttpRequest
# {"total":28,"rows":[{"productid":"FI-SW-01","productname":"Koi","unitcost":10.00,"status":"P","listprice":36.50,"attr1":"Large","itemid":"EST-1"}]}

class utils():

    # 获取 snowui-datagrid json格式数据源
    # 黄耀樑 2016-07-22
    def getDatagrid(query=[]):                    
        return {"total":0,"rows":query}

    # 封装表单数据到实体
    # 黄耀樑 2016-07-26
    def createObject(model, request, exclude=[]):                    
        for x in request.POST:
            if x in model._meta.get_all_field_names():
                if exclude and not x in exclude:
                    setattr(model, x, request.POST[x])

