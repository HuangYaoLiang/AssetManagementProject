#coding:utf-8

"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime

import app.forms
import app.models
import os
import posixpath
from AssetManagementProject import settings
 

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
        if ids is not None:
            for id in ids.split(','):
               app.models.LikeImageInfo.objects.create(pc_ip=user_ip,img_number=id)
    user_img = app.models.LikeImageInfo.objects.filter(pc_ip=user_ip)
    return render(request,
        'app/temporary/imagelist.html',
        {
            'title': '活动图片投票',
            'user_imgCount':user_img.count(),
            'user_imgIDS':user_img.values_list('img_number', flat=True),
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
def hardware(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST': 
        form = app.forms.HardwareForm(request.POST) 
        if form.is_valid():            
            app.models.HardwareInfo(serial_number = form.cleaned_data['serial_number'],
                person_id = form.cleaned_data['person_id'],
                position = form.cleaned_data['position'],
                system_os = form.cleaned_data['system_os'],
                pc_score = form.cleaned_data['pc_score'],
                pc_cpu = form.cleaned_data['pc_cpu'],
                pc_memory = form.cleaned_data['pc_memory'],
                pc_description = form.cleaned_data['pc_description'],
                use_time = form.cleaned_data['use_time'],).save()
 
    return render(request,
        'app/hardware.html',
        {
            'title': '硬件信息',
            'form': app.forms.HardwareForm(), #获得表单对象
        })

# 打印机信息
def printer(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST': 
        form = app.forms.PrinterForm(request.POST) 
        if form.is_valid():
            app.models.PrinterInfo(serial_number = form.cleaned_data['serial_number'],
                person_id = form.cleaned_data['person_id'],
                position = form.cleaned_data['position'],
                prt_model = form.cleaned_data['prt_model'],
                prt_description = form.cleaned_data['prt_description'],
                use_time = form.cleaned_data['use_time'],).save()
 
    return render(request,
        'app/printer.html',
        {
            'title': '打印机信息',
            'form': app.forms.PrinterForm(), #获得表单对象
        })

# 职员信息
def person(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST': 
        form = app.forms.PersonForm(request.POST) 
        if form.is_valid():            
            app.models.PersonInfo(name = form.cleaned_data['name'],
                position = form.cleaned_data['position'],
                contact = form.cleaned_data['contact'],
                pc_mac = form.cleaned_data['pc_mac'],
                pc_ip = form.cleaned_data['pc_ip'],).save()
 
    return render(request,
        'app/person.html',
        {
            'title': '职员信息',
            'form': app.forms.PersonForm(), #获得表单对象
        })

# 变更记录
def log(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST': 
        form = app.forms.LogForm(request.POST) 
        if form.is_valid():            
            app.models.ChangeLog(serial_number = form.cleaned_data['serial_number'],
                name = form.cleaned_data['name'],
                type = form.cleaned_data['type'],
                remark = form.cleaned_data['remark'],).save() 
    return render(request,
        'app/log.html',
        {
            'title': '变更记录',
            'form': app.forms.LogForm(), #获得表单对象
            'data':app.models.ChangeLog.objects.all()
        })