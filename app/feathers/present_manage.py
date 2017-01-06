# coding:utf8
# @author:nick
# @company:joyme
from . import BaseFeather
from app.models.feather_models import PresentSendActivity
from app.models.feather_models import Present as PresentModel


class Present(BaseFeather):
    """实现发放礼包功能"""
    """一个用户只能领1次"""
    """每天发多少不做限制"""
    """活动能随时关停"""
    """活动能配置结束提示语"""
    """活动能配置礼包发放完提示语"""

    """能查询剩余多少未发，可以追加"""
    """只能通过菜单栏、关键字领取"""

    def get_response(self):
        self.response_type = 'text'
        # 判断当前是否有开启状态的活动
        try:
            activity = PresentSendActivity.objects.get(status=True, public=self.public_instance)
        except PresentSendActivity.DoesNotExist:
            return u'当前暂时没有获得'

        from django.utils import timezone
        datetime_now = timezone.now()
        start_time = activity.start_date
        end_time = activity.end_date
        if datetime_now < start_time:
            return activity.not_start_prompt
        if datetime_now > end_time:
            return activity.end_prompt

        if PresentModel.objects.filter(activity=activity, receiver_follower=self.follower_instance):
            # 判断当前用户是否已领取
            return activity.duplicate_prompt

        last_codes = PresentModel.objects.filter(activity=activity, status=False)
        if last_codes:
            code_instance = last_codes[0]
            code_instance.received_time = datetime_now
            code_instance.receiver_follower = self.follower_instance
            code_instance.status = True
            code_instance.save()
            return code_instance.exchange_code
        else:
            return activity.exceed_prompt


class Test(BaseFeather):
    """Test"""

    def get_response(self):
        """
        :return:
        """
        self.response_type = 'text'
        return u'啪啪以啪啪 啊啊啊啊啊 摩擦以摩擦 啊啊啊啊啊'
