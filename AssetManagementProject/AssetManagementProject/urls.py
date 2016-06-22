"""
Definition of urls for AssetManagementProject.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # 测试
    url(r'^test', app.views.test, name='test'),
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^hardware$', app.views.hardware, name='hardware'),
    url(r'^printer$', app.views.printer, name='printer'),
    url(r'^person$', app.views.person, name='person'),
    url(r'^log$', app.views.log, name='log'),
    url(r'^login/$',
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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    
    
]
