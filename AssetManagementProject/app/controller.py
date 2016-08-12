"""
控制器
黄耀樑 2016-07-20
"""

import json
import re
import sys

from django.http.response import JsonResponse
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from app.utils import utils
from app.models import *


# {"total":28,"rows":[{"productid":"FI-SW-01","productname":"Koi","unitcost":10.00,"status":"P","listprice":36.50,"attr1":"Large","itemid":"EST-1"}]}
class controller():

    # 查询实体
    # 黄耀樑 2016-07-26
    def get(request, key, id=0):
        # key = request.GET.get('key') # key不存在返回None,还能给默认值
        # key = request.GET['key'] # key不存在就会产生异常
        obj = {}
        if key:
            model = {}
            if key == 'printer':
                model = AssetInfo()
            elif key == 'hardware2':
                model = HardwareInfo()
            else:
                model = utils.importModel(key)()
            # 获取模块数据
            if id and int(id) > 0:
                obj = model.getOne(id)
            else:
                obj = utils.toJsonObject(model)
        return JsonResponse(obj)
    
    # 查询列表
    # 黄耀樑 2016-07-20
    def query(request, key):
        # key = request.GET.get('key') # key不存在返回None,还能给默认值
        # key = request.GET['key'] # key不存在就会产生异常
        query = []
        sqlWhere = None
        sortName = request.GET.get('sortName')
        sortOrder = request.GET.get('sortOrder')
        searchName = request.GET.get('searchName')
        searchVal = request.GET.get('searchVal')
        # 通用查询
        if searchName and searchVal:
            sqlWhere = ''
            for x in searchName.split(','):
                if sqlWhere:
                    sqlWhere += ' OR '
                sqlWhere += ("%s LIKE '%%%s%%'" % (x, searchVal))
        if sqlWhere:
            sqlWhere = '(' + sqlWhere + ')'
        if key:
            pc_state = request.GET.get('pc_state')
            stateWhere = ''
            if pc_state and key in ['printer', 'hardware', 'hardware2']:
                if pc_state == '1':
                    if key == 'printer':
                        stateWhere = "position<>'106'"
                    else:
                        stateWhere = "person_id>0"
                elif pc_state == '2':
                    if key == 'printer':
                        stateWhere = "position='106'"
                    else:
                        stateWhere = "(person_id=0 AND state='OK')"
                elif pc_state == '3':
                    stateWhere = "state='BAD'"
                elif pc_state == '4':
                    stateWhere = "state='SCRAP'"
                elif pc_state == '5':
                    stateWhere = "state='UNKNOWN'"
                if sqlWhere:
                    sqlWhere += (' AND ' + stateWhere)
                else:
                    sqlWhere = stateWhere
            if key == 'printer':
                printerWhere = "category IN ('多功能一体机','打印设备','复印机')"
                if sqlWhere:
                    sqlWhere += (" AND " + printerWhere)
                else:
                    sqlWhere = printerWhere
                query = AssetInfo().getList(sqlWhere, sortName, sortOrder)
            elif key == 'hardware':
                
                if pc_state == '6':
                    query = HardwareInfo().getServerList(sqlWhere, sortName, sortOrder)
                else:
                    query = HardwareInfo().getDesktopList(sqlWhere, sortName, sortOrder)
            elif key == 'hardware2':
                query = HardwareInfo().getNotebookList(sqlWhere, sortName, sortOrder)
            #elif key == 'untread':
            #    pass
            else:
                query = utils.importModel(key)().getList(sqlWhere, sortName, sortOrder)
        return JsonResponse(utils.getDatagrid(query))

    # 新增或者更新
    # 黄耀樑 2016-07-22
    def edit(request, key):
        success = True
        msg = '操作成功！'
        if key:
            try:            
                id = int(request.POST.get('id', 0))
                if key == 'hardware' or key == 'hardware2':
                    assetInfo = AssetInfo()
                    hardwareInfo = HardwareInfo()
                    if id > 0:
                        assetInfo = AssetInfo.objects.get(id=id)
                        hardwareInfo = HardwareInfo.objects.get(asset_id=id)
                    utils.createObject(assetInfo, request)
                    utils.createObject(hardwareInfo, request)
                    assetInfo.save()
                    hardwareInfo.asset_id = assetInfo.id
                    hardwareInfo.save()
                elif key == 'printer':
                    assetInfo = AssetInfo()
                    if id > 0:
                        assetInfo = AssetInfo.objects.get(id=id)
                    utils.createObject(assetInfo, request)
                    assetInfo.save()
                elif key == 'change':
                    state = request.POST['state']                    
                    changeInfo = ChangeInfo()
                    if id > 0:
                        changeInfo = ChangeInfo.objects.get(id=id)
                    utils.createObject(changeInfo, request)
                    # 添加的时候要特别处理
                    if changeInfo.type == '硬件更换' and id == 0:
                        remark = request.POST['remark']
                        changeInfo1 = ChangeInfo()
                        utils.createObject(changeInfo1, request)
                        changeInfo1.serial_number = request.POST['serial_number2']
                        changeInfo1.name = request.POST['name2']
                        changeInfo1.position = request.POST['position2']
                        changeInfo1.remark = '因为 %s 位置(%s)使用者(%s)编号(%s)，调整到，位置(%s)使用者(%s)编号(%s)' % (remark, changeInfo1.position, changeInfo1.name,changeInfo1.serial_number, changeInfo.position, changeInfo.name, changeInfo.serial_number)
                        if len(changeInfo1.serial_number) >= 6 and state == '0':
                            changeInfo1.state = state
                        changeInfo1.save()
                        changeInfo.remark = '因为 %s 位置(%s)使用者(%s)编号(%s)，调整到，位置(%s)使用者(%s)编号(%s)' % (remark, changeInfo.position, changeInfo.name,changeInfo.serial_number, changeInfo1.position, changeInfo1.name, changeInfo1.serial_number)
                    if len(changeInfo.serial_number) >= 6 and state == '0':
                        changeInfo.state = 0
                    else:
                        changeInfo.state = -1
                    changeInfo.save()
                elif key == 'untread':
                    untreadInfo = UntreadInfo()                    
                    if id > 0:
                        untreadInfo = UntreadInfo.objects.get(id=id)
                        UntreadDetailInfo.objects.filter(untread_id=id).delete()
                    untreadInfo.untread_time = request.POST['untread_time']
                    untreadInfo.remark = request.POST['remark']
                    untreadInfo.save()
                    count = int(request.POST['UntreadCount'])
                    i = 0
                    while i < count:
                        j = str(i)   
                        if 'category' + j in request.POST:                 
                            untreadDetailInfo = UntreadDetailInfo()
                            untreadDetailInfo.untread_id = untreadInfo.id
                            untreadDetailInfo.category = request.POST['category' + j]
                            untreadDetailInfo.serial_number = request.POST['serial_number' + j]
                            untreadDetailInfo.name = request.POST['name' + j]
                            untreadDetailInfo.reason = '无法使用'
                            untreadDetailInfo.remark = '106室'
                            untreadDetailInfo.save()
                        i += 1
                else:
                    obj = {}
                    model = utils.importModel(key)
                    if id > 0:
                        obj = model.objects.get(id=id)
                    else:
                        obj = model()
                    utils.createObject(obj, request)
                    obj.save()
            except:
                info = sys.exc_info()  
                success = False
                msg = '操作失败！'
        return JsonResponse({'success': success, 'msg': msg})

    # 删除
    # 黄耀樑 2016-07-22
    def remove(request, key):
        success = True
        msg = '操作成功！'
        try:
            ids = request.POST["ids"]
            if key and ids:
                if key == 'printer':
                    AssetInfo.objects.extra(where=['id IN (%s)' % ids]).delete()
                elif key == 'hardware' or key == 'hardware2':
                    AssetInfo.objects.extra(where=['id IN (%s)' % ids]).delete()
                    HardwareInfo.objects.extra(where=['asset_id IN (%s)' % ids]).delete()
                elif key == 'untread':
                    UntreadInfo.objects.extra(where=['id IN (%s)' % ids]).delete()
                    UntreadDetailInfo.objects.extra(where=['untread_id IN (%s)' % ids]).delete()
                else:
                    model = utils.importModel(key)
                    model.objects.extra(where=['id IN (%s)' % ids]).delete()
        except:
            success = False
            msg = '操作失败！'
        return JsonResponse({'success': success, 'msg': msg})

