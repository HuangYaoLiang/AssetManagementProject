#coding:utf-8

"""
视图类
黄耀樑 2016-07-20
"""

import app.forms
import app.models
import os
import posixpath
import json

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime,timedelta
from AssetManagementProject import settings
from django.http.response import JsonResponse


# 测试
def test(request):
    # request[0]+request[1]
    assert isinstance(request, HttpRequest)
    return HttpResponse(str(int(request.GET['a']) + int(request.GET['b'])))

# 活动图片投票
def imagelist(request):
    assert isinstance(request, HttpRequest)
    user_ip = request.META['REMOTE_ADDR']
    likeImageInfo = app.models.LikeImageInfo()
    if request.method == 'POST': 
        ids = request.POST.get('ids')
        app.models.LikeImageInfo.objects.filter(pc_ip=user_ip).delete()
        if ids:
            for id in ids.split(','):
               app.models.LikeImageInfo.objects.create(pc_ip=user_ip,img_number=id)
    user_img = app.models.LikeImageInfo.objects.filter(pc_ip=user_ip)
    return render(request,
        'app/temporary/imagelist.html',
        {
            'title': '活动图片投票',
            'user_imgCount':user_img.count(),
            'user_imgIDS':user_img.values_list('img_number', flat=True), # 只有一列的话 可以使用flat=True，多列会出错
            'all_img': os.listdir(settings.STATIC_ROOT + '/app/temporary/img/list'),
            'request_ip':request.META['REMOTE_ADDR'],
        })

# 首页
def home(request):
    # assert isinstance(request, HttpRequest)
    return render(request, 'app/index.html', {
            'title': '首页',
            'dateTest': '2016.08.01',
    })

# 台式机信息列表
# 黄耀樑 2016-07-26
def hardwareList(request):
    return render(request,'app/hardware/hardwareList.html',{
            'title': '硬件信息',
            'menu': 'hardware',
            'maxNo':app.models.HardwareInfo().getMaxNumber("category='台式机'"),
    })

# 台式机信息详细
# 黄耀樑 2016-07-26
def hardwareDetail(request, id=0):
    dsPerson = app.models.PersonInfo().getDropDownList()
    return render(request,'app/hardware/hardwareDetail.html',{
        'title': '硬件信息',
        'menu': 'hardware',
        'id': id if id else 0,
        'dsPerson': dsPerson,
    })

# 笔记本信息列表
# 黄耀樑 2016-07-26
def hardware2List(request):
    return render(request,'app/hardware/hardware2List.html',{
            'title': '硬件信息',
            'menu': 'hardware2',
    })

# 笔记本信息详细
# 黄耀樑 2016-07-26
def hardware2Detail(request, id=0):
    dsPerson = app.models.PersonInfo().getDropDownList()
    return render(request,'app/hardware/hardware2Detail.html',{
        'title': '硬件信息',
        'menu': 'hardware2',
        'id': id if id else 0,
        'dsPerson': dsPerson,
    })

# 打印机信息列表
# 黄耀樑 2016-07-26
def printerList(request):
    return render(request,'app/printer/printerList.html',{
            'title': '打印机信息',
            'menu': 'printer',
            'maxNo': app.models.AssetInfo().getMaxNumber("category IN ('多功能一体机','打印设备','复印机')"),
    })

# 打印机信息详细
# 黄耀樑 2016-07-26
def printerDetail(request, id=0):
    dsPerson = app.models.PersonInfo().getDropDownList()
    return render(request,'app/printer/printerDetail.html',{
        'title': '打印机信息',
        'menu': 'printer',
        'id': id if id else 0,
        'dsPerson': dsPerson,
    })

# 职员信息列表
# 黄耀樑 2016-07-26
def personList(request):
    return render(request,'app/person/personList.html',{
            'title': '职员信息',
            'menu': 'person',
    })

# 职员信息详细
# 黄耀樑 2016-07-26
def personDetail(request, id=0):
    return render(request,'app/person/personDetail.html',{
        'title': '职员信息',
        'menu': 'person',
        'id': id if id else 0,
    })

# 变更记录列表
# 黄耀樑 2016-07-26
def changeList(request):
    return render(request,'app/change/changeList.html',{
            'title': '变更记录',
            'menu': 'change',
    })

# 变更记录详细
# 黄耀樑 2016-07-26
def changeDetail(request, id=0):
    return render(request,'app/change/changeDetail.html',{
        'title': '变更记录',
        'menu': 'change',
        'id': id if id else 0,
    })

# 退回记录列表
# 黄耀樑 2016-08-10
def untreadList(request):
    return render(request,'app/untread/untreadList.html',{
            'title': '退回记录',
            'menu': 'untread',
    })

# 退回记录详细
# 黄耀樑 2016-08-10
def untreadDetail(request, id=0):
    id = id if id else 0
    return render(request,'app/untread/untreadDetail.html',{
        'title': '退回记录',
        'menu': 'untread',
        'id': id,
        'data': app.models.UntreadDetailInfo.objects.filter(untread_id=id)
    })

# 任务列表
# 黄耀樑 2016-07-26
def task(request):
    assert isinstance(request, HttpRequest)
    error = ''
    id = 0
    if request.method == 'POST':
        form = app.forms.LogForm(request.POST)
        id = form.data['hdnID'] # 这个值是隐藏域的 用以判断是添加还是修改
        ids = form.data['hdnIDS'] # 这个值是隐藏域的 用以删除
        if ids:            
            app.models.ChangeLog.objects.extra(where=['id IN (%s)' % ids]).delete()
            id = -1
        else:
            if form.is_valid():            
                if id and id != '0':
                    model = app.models.ChangeLog.objects.get(id=id)
                else:
                    model = app.models.ChangeLog()
                model.serial_number = form.cleaned_data['serial_number']
                model.create_time = form.cleaned_data['create_time']
                model.name = form.cleaned_data['name']
                model.type = form.cleaned_data['type']
                model.remark = form.cleaned_data['remark']
                if len(model.serial_number) >= 8:
                    model.state = 0
                else:
                    model.state = -1
                model.save()
                id = -1 
            else:
                error = 1
    else:
        if id and id != '0':  # 这个值是url get过来的 用以初始化编辑
            form = app.forms.LogForm(instance = app.models.ChangeLog.objects.get(id=id))
        else:
            form = app.forms.LogForm()
            id = 0
    return render(request,'app/task.html',{
            'title': '任务列表',
            'form': form, #获得表单对象
            'data':app.models.ChangeLog.objects.all().order_by('-create_time'), # 字段前面的减号是降序排列
            'id': id,
            'error': error,
            })