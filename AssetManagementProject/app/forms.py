"""
Definition of forms.
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
class HardwareForm(ModelForm):
  class Meta:
    model = app.models.HardwareInfo
    fields = '__all__'

# 打印机表单
class PrinterForm(ModelForm):
  class Meta:
    model = app.models.PrinterInfo
    fields = '__all__'

# 职员表单
class PersonForm(ModelForm):
  class Meta:
    model = app.models.PersonInfo
    fields = '__all__'

# 变更表单
class LogForm(ModelForm):
  class Meta:
    model = app.models.ChangeLog
    fields = '__all__'


