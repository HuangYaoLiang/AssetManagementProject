"""
Definition of urls for AssetManagementProject.
"""

import app.forms
import app.views
import app.controller
import django.contrib.auth.views

from datetime import datetime
from django.conf.urls import url

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # 测试
    url(r'^test', app.views.test, name='test'),
    # 临时页面
    # url(r'^imagelist$', app.views.imagelist, name='imagelist'),
    # Examples:
    url(r'^$', app.views.home, name='home'),

    #url(r'^hardware(/(?P<id>-?\d{1,})(/(?P<sort>\w{1,})/(?P<order>\w{1,}))?)?$', app.views.hardware, name='hardware'),
    #url(r'^printer(/(?P<id>-?\d{1,}))?$', app.views.printer, name='printer'),
    #url(r'^person(/(?P<id>\d{1,}))?$', app.views.person, name='person'),
    #url(r'^log(/(?P<id>\d{1,}))?$', app.views.log, name='log'),

    url(r'^hardwareList$', app.views.hardwareList, name='hardwareList'),
    url(r'^hardwareDetail/(\d*)$', app.views.hardwareDetail, name='hardwareDetail'),
    url(r'^hardware2List$', app.views.hardware2List, name='hardware2List'),
    url(r'^hardware2Detail/(\d*)$', app.views.hardware2Detail, name='hardware2Detail'),
    url(r'^hardware3List$', app.views.hardware3List, name='hardware3List'),
    url(r'^hardware3Detail/(\d*)$', app.views.hardware3Detail, name='hardware3Detail'),
    url(r'^printerList$', app.views.printerList, name='printerList'),
    url(r'^printerDetail/(\d*)$', app.views.printerDetail, name='printerDetail'),
    url(r'^personList$', app.views.personList, name='personList'),
    url(r'^personDetail/(\d*)$', app.views.personDetail, name='personDetail'),
    url(r'^changeList$', app.views.changeList, name='changeList'),
    url(r'^changeDetail/(\d*)$', app.views.changeDetail, name='changeDetail'),
    url(r'^untreadList$', app.views.untreadList, name='untreadList'),
    url(r'^untreadDetail/(\d*)$', app.views.untreadDetail, name='untreadDetail'),

    url(r'^task$', app.views.task, name='task'),

    url(r'^login$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    
    # 控制器操作
    url(r'^get/(\w+)/(\d*)$', app.controller.controller.get, name='get'),
    url(r'^query/(\w+)$', app.controller.controller.query, name='query'),
    url(r'^edit/(\w+)$', app.controller.controller.edit, name='edit'),
    url(r'^remove/(\w+)$', app.controller.controller.remove, name='remove'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
