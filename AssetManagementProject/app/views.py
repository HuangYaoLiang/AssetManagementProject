#coding:utf-8

"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from AssetManagementProject import settings
from django.http.response import JsonResponse

import app.forms
import app.models
import os
import posixpath
import json


# 测试
def test(request):
    # request[0]+request[1]
    assert isinstance(request, HttpRequest)
    return HttpResponse(str(int(request.GET['a']) + int(request.GET['b'])))

# 活动图片投票
def imagelist(request):
    assert isinstance(request, HttpRequest)
    user_ip = request.META['REMOTE_ADDR']
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
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title': '首页',
        })

# 硬件信息
def hardware(request, id=0, sort='', order=''):
    assert isinstance(request, HttpRequest)
    error = ''
    if request.method == 'POST':
        form = app.forms.HardwareForm(request.POST)
        id = form.data['hdnID'] # 这个值是隐藏域的 用以判断是添加还是修改
        ids = form.data['hdnIDS'] # 这个值是隐藏域的 用以删除
        if ids:            
            app.models.HardwareInfo.objects.extra(where=['id IN (%s)' % ids]).delete()
            id = -1
        else:
            if form.is_valid():            
                if id and id != '0':
                    model = app.models.HardwareInfo.objects.get(id=id)
                else:
                    model = app.models.HardwareInfo()

                model.serial_number = form.cleaned_data['serial_number']
                model.person_id = form.cleaned_data['person_id']
                model.position = form.cleaned_data['position']
                model.system_os = form.cleaned_data['system_os']
                model.pc_score = form.cleaned_data['pc_score']
                model.pc_cpu = form.cleaned_data['pc_cpu']
                model.pc_memory = form.cleaned_data['pc_memory']
                model.pc_description = form.cleaned_data['pc_description']
                model.use_time = form.cleaned_data['use_time']
                model.pc_mac = form.cleaned_data['pc_mac']
                model.pc_ip = form.cleaned_data['pc_ip']
                model.save()
                id = -1 
            else:
                error = 1
    else:
        if id and id != '0':  # 这个值是url get过来的 用以初始化编辑
            form = app.forms.HardwareForm(instance = app.models.HardwareInfo.objects.get(id=id))
        else:
            form = app.forms.HardwareForm()
            id = 0  

    if not sort:
        sort = 'pc_score'  
    if not order:
        order = ''
    data = app.models.HardwareInfo().getHardwareList(sort,order) 
    return render(request,'app/hardware.html',{
            'title': '硬件信息',
            'form': form, #获得表单对象
            'data': data,
            'error': error,
            'id': id,
            'order': order,
            'sort': sort,
            })

# 打印机信息
def printer(request,id=0):
    assert isinstance(request, HttpRequest)
    error = ''
    if request.method == 'POST':
        form = app.forms.PrinterForm(request.POST)
        id = form.data['hdnID'] # 这个值是隐藏域的 用以判断是添加还是修改
        ids = form.data['hdnIDS'] # 这个值是隐藏域的 用以删除
        if ids:            
            app.models.PrinterInfo.objects.extra(where=['id IN (%s)' % ids]).delete()
            id = -1
        else:
            if form.is_valid():            
                if id and id != '0':
                    model = app.models.PrinterInfo.objects.get(id=id)
                else:
                    model = app.models.PrinterInfo()

                model.serial_number = form.cleaned_data['serial_number']
                model.person_id = form.cleaned_data['person_id']
                model.position = form.cleaned_data['position']
                model.prt_model = form.cleaned_data['prt_model']
                model.prt_description = form.cleaned_data['prt_description']
                model.use_time = form.cleaned_data['use_time']
                model.save()
                id = -1
            else:
                error = 1
    else:
        if id and id != '0':  # 这个值是url get过来的 用以初始化编辑
            form = app.forms.PrinterForm(instance = app.models.PrinterInfo.objects.get(id=id))
        else:
            form = app.forms.PrinterForm()
            id = 0
    return render(request,'app/printer.html',{
            'title': '打印机信息',
            'form': form, #获得表单对象
            'data':app.models.PrinterInfo().getPrinterList(),
            'id': id,
            'error': error,
            })

# 职员信息
def person(request,id=0):
    assert isinstance(request, HttpRequest)
    error = ''
    if request.method == 'POST':
        form = app.forms.PersonForm(request.POST)
        id = form.data['hdnID'] # 这个值是隐藏域的 用以判断是添加还是修改
        ids = form.data['hdnIDS'] # 这个值是隐藏域的 用以删除
        if ids:            
            app.models.PersonInfo.objects.extra(where=['id IN (%s)' % ids]).delete()
            id = -1
        else:
            if form.is_valid():            
                if id and id != '0':
                    model = app.models.PersonInfo.objects.get(id=id)
                else:
                    model = app.models.PersonInfo()

                model.name = form.cleaned_data['name']
                model.position = form.cleaned_data['position']
                model.contact = form.cleaned_data['contact']
                #model.pc_mac = form.cleaned_data['pc_mac']
                #model.pc_ip = form.cleaned_data['pc_ip']
                model.save()
                id = -1 
            else:
                error = 1
    else:
        if id and id != '0':  # 这个值是url get过来的 用以初始化编辑
            form = app.forms.PersonForm(instance = app.models.PersonInfo.objects.get(id=id))
        else:
            form = app.forms.PersonForm()
            id = 0
    data = app.models.PersonInfo.objects.all().order_by('position', 'name')
    return render(request,'app/person.html',{
            'title': '职员信息',
            'form': form, #获得表单对象
            'data': data,
            'id': id,
            'error': error,
            })

# 变更记录
def log(request,id=0):
    assert isinstance(request, HttpRequest)
    error = ''
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

                model.create_time = form.cleaned_data['create_time']
                model.serial_number = form.cleaned_data['serial_number']
                model.name = form.cleaned_data['name']
                model.type = form.cleaned_data['type']
                model.remark = form.cleaned_data['remark']
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
    return render(request,'app/log.html',{
            'title': '变更记录',
            'form': form, #获得表单对象
            'data':app.models.ChangeLog.objects.all().order_by('-create_time'), # 字段前面的减号是降序排列
            'id': id,
            'error': error,
            })