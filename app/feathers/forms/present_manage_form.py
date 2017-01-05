# coding:utf8
# @author:nick
# @company:joyme

from django.forms.models import ModelForm

from app.models.feather_models import PresentSendActivity
from  bootstrap3_datetime.widgets import DateTimePicker
from django import forms


class PresentForm(ModelForm):
    class Meta:
        model = PresentSendActivity
        exclude = ['create_user', 'public']
        widgets = {
            'start_date': DateTimePicker(
                options={"format": "YYYY-MM-DD HH:mm:ss", 'pickTime': True, 'language': 'zh-CN'}),
            'end_date': DateTimePicker(
                options={"format": "YYYY-MM-DD HH:mm:ss", 'pickTime': True, 'language': 'zh-CN'}),
            'duplicate_prompt': forms.Textarea(attrs={'rows': 5}),
            'exceed_prompt': forms.Textarea(attrs={'rows': 5}),
            'end_prompt': forms.Textarea(attrs={'rows': 5}),
            'not_start_prompt': forms.Textarea(attrs={'rows': 5}),
            'name': forms.TextInput(attrs={'style': 'width:100%'})

        }


class PresentCodeImportForm(forms.Form):
    """激活码上传"""
    codes = forms.FileField(label='上传文件', help_text=u'txt格式,每个激活码独占1行')
