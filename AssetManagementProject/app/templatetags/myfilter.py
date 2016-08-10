#! /usr/bin/python
# coding=utf-8

"""
自定义过滤器
黄耀樑 2016-07-20
"""

from django import template
from datetime import datetime,timedelta

register = template.Library()

@register.filter
def key(d,key_name):
    value = 0
    try:
        value = d[key_name]
    except KeyError:
        value = 0
    return value

@register.filter
def isNew(dateValue):
    newSpan = ''     
    date1 = (datetime.strptime(dateValue, "%Y.%m.%d").date() + timedelta(days = 15))
    nowDate = datetime.now().date()
    if date1 >= nowDate:
        newSpan = '<img class="new-a" src="static/images/home/new_a.gif" />'  
    return newSpan

#register.filter('isNew',isNew)
#register.filter('key',key)