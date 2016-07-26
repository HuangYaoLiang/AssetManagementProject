"""
表单类
黄耀樑 2016-07-20
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

import app.models

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

# 硬件表单
#class HardwareForm(ModelForm):
#    class Meta:
#        model = app.models.HardwareInfo
#        # 不用 __all__ 是为了界面的排序显示
#        fields = '__all__'
        #'serial_number','person_id','position','system_os','pc_score','pc_cpu','pc_memory','pc_mac','pc_ip','price','use_time','pc_description', 'remark'
    #def __init__(self, *args, **kwargs):
        #super(HardwareForm, self).__init__(*args, **kwargs)
        #self.fields['serial_number'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['person_id'].widget = forms.Select({'class': 'form-control'},choices= app.models.PersonInfo().getPersonDropDownList())
        #self.fields['position'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['system_os'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['pc_score'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['pc_cpu'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['pc_memory'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['pc_description'].widget = forms.Textarea({'class': 'form-control','style':'height:200px;'})
        #self.fields['price'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['use_time'].widget = forms.TextInput({'class': 'form-control form-datetime'})
        #self.fields['pc_mac'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['pc_ip'].widget = forms.TextInput({'class': 'form-control'})
        #self.fields['remark'].widget = forms.TextInput({'class': 'form-control'})

## 打印机表单
#class PrinterForm(ModelForm):
#    class Meta:
#        model = app.models.PrinterInfo
#        fields = '__all__'
    #def __init__(self, *args, **kwargs):
    #    super(PrinterForm, self).__init__(*args, **kwargs)
    #    self.fields['serial_number'].widget = forms.TextInput({'class': 'form-control'})
    #    self.fields['person_id'].widget = forms.Select({'class': 'form-control'},choices= app.models.PersonInfo().getPersonDropDownList())
    #    self.fields['position'].widget = forms.TextInput({'class': 'form-control'})
    #    self.fields['prt_model'].widget = forms.TextInput({'class': 'form-control'})
    #    self.fields['prt_description'].widget = forms.Textarea({'class': 'form-control'})
    #    self.fields['use_time'].widget = forms.TextInput({'class': 'form-control form-datetime'})
    #    self.fields['price'].widget = forms.TextInput({'class': 'form-control'})
    #    self.fields['remark'].widget = forms.TextInput({'class': 'form-control'})

## 职员表单
#class PersonForm(ModelForm):
#    class Meta:
#        model = app.models.PersonInfo
#        fields = '__all__'
#    def __init__(self, *args, **kwargs):
#        super(PersonForm, self).__init__(*args, **kwargs)
#        self.fields['name'].widget = forms.TextInput({'class': 'form-control'})
#        self.fields['position'].widget = forms.TextInput({'class': 'form-control'})
#        self.fields['contact'].widget = forms.TextInput({'class': 'form-control'})
#        self.fields['remark'].widget = forms.TextInput({'class': 'form-control'})

## 变更表单
#class LogForm(ModelForm):
#    # 1.  这是全新构建一个html控件
#    # serial_number = forms.CharField(widget=forms.TextInput({'class':
#    # 'form-control'}),)
#    class Meta:
#        model = app.models.ChangeLog
#        fields = ('serial_number', 'name', 'type', 'remark', 'create_time')
#        # fields = '__all__' # 如果要调整模版界面的字段显示的顺序 这里就要单独写了 ('x1', 'x2')
#        #widgets={'serial_number':forms.TextInput({'class': 'form-control'}),}
#                                  ## 2.  这是改写model里面字段的
#    # 3.  这也是改写model里面字段的
#    def __init__(self, *args, **kwargs):
#        super(LogForm, self).__init__(*args, **kwargs)
#        self.fields['serial_number'].widget = forms.TextInput({'class': 'form-control'})
#        self.fields['name'].widget = forms.TextInput({'class': 'form-control'})
#        self.fields['type'].widget = forms.TextInput({'class': 'form-control'})
#        self.fields['remark'].widget = forms.Textarea({'class': 'form-control'})
#        self.fields['create_time'].widget = forms.TextInput({'class': 'form-control form-datetime'})

