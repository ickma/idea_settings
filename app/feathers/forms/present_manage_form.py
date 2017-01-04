# coding:utf8
# @author:nick
# @company:joyme

from django.forms.models import ModelForm
from django.forms.utils import ErrorList

from app.models.feather_models import PresentSendActivity
from  bootstrap3_datetime.widgets import DateTimePicker


class PresentForm(ModelForm):
    class Meta:
        model = PresentSendActivity
        exclude = ['create_user', 'public']
        widgets = {
            'start_date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm:SS", 'pickTime': False,'language':'zh-CN'})
        }

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        super(PresentForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                          empty_permitted, instance, use_required_attribute)
        for _, v in self.fields.items():
            v.widget.attrs['style'] = 'width:30%'
