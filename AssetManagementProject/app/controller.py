"""
控制器
黄耀樑 2016-07-20
"""


from django.http.response import JsonResponse
from django.http import HttpRequest
#from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from app.utils import utils

import json
import app.models
#import app.utils



# {"total":28,"rows":[{"productid":"FI-SW-01","productname":"Koi","unitcost":10.00,"status":"P","listprice":36.50,"attr1":"Large","itemid":"EST-1"}]}
class controller():

    # 查询实体
    # 黄耀樑 2016-07-26
    def get(request, key, id=0):
        # key = request.GET.get('key') # key不存在返回None,还能给默认值
        # key = request.GET['key'] # key不存在就会产生异常
        obj = {}
        if id and int(id) > 0:
            if key == 'hardware':
                obj = app.models.HardwareInfo().getOne(id)
            elif key == 'person':
                obj = app.models.PersonInfo().getOne(id)
        return JsonResponse(obj)
    
    # 查询列表
    # 黄耀樑 2016-07-20
    def query(request, key):
        # key = request.GET.get('key') # key不存在返回None,还能给默认值
        # key = request.GET['key'] # key不存在就会产生异常
        query = []
        if key == 'hardware':
            query = app.models.HardwareInfo().getList()
        elif key == 'person':
            query = app.models.PersonInfo().getList()
        return JsonResponse(utils.getDatagrid(query))

    # 新增或者更新
    # 黄耀樑 2016-07-22
    def edit(request, key):
        #assert isinstance(request, HttpRequest)
        # user_obj=json.loads(request.body.decode())
        success = True
        msg = '操作成功'
        id = int(request.POST.get('id', 0))
        if key == 'hardware':
            assetInfo = app.models.AssetInfo()
            hardwareInfo = app.models.HardwareInfo()
            if id > 0:
                assetInfo = app.models.AssetInfo.objects.get(id=id)
                hardwareInfo = app.models.HardwareInfo.objects.get(asset_id=id)
            utils.createObject(assetInfo, request)
            utils.createObject(hardwareInfo, request, ['id'])
            # assetInfo.save()
        elif key == 'person':
            personInfo = app.models.PersonInfo()
            if id > 0:
                personInfo = app.models.PersonInfo.objects.get(id=id)
            utils.createObject(personInfo, request)
            personInfo.save()
        return JsonResponse({'success': success, 'msg': msg})

