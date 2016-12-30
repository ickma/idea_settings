# coding:utf8
# @author:nick
# @company:joyme
import math

from . import register
from django.db.models.query import QuerySet
from django import template


@register.filter(name='create_action')
def create_action(line_data):
    """

    :param line_data:
    :return:
    """
    return """
    <div class="btn-group">
                  <button type="button" class="btn btn-info">操作</button>
                  <button type="button" class="btn btn-info dropdown-toggle" data-toggle="dropdown" aria-expanded="false">
                    <span class="caret"></span>
                  </button>
                  <ul class="dropdown-menu" role="menu">
                    <li><a href="?action=edit&id={0}">编辑</a></li>
                    <li><a href="?action=delete&id={0}">删除</a></li>
                  </ul>
                </div>
    """.format(line_data.id)


@register.simple_tag(name='create_show_index', takes_context=True)
def create_show_index(context, counter):
    """
    生成用于显示的id
    将数据库中的id进行重新排序
    :param counter: 
    :param context: 
    :return:
    """
    table_datas = context['table_datas']
    """:type :QuerySet"""
    data_length = table_datas.count()

    request = context['request']
    page = int(request.GET.get('page', 1))
    pc = context['pc']
    return data_length - (((page - 1) * pc) + counter) + 1


@register.filter(name="create_choose_html")
def create_choose_html(instance):
    """

    :param instance:
    :return:
    """
    return """
      <td data-delete-id="{0}"><input type="checkbox" title=""></td>
    """.format(instance.id)


@register.simple_tag(name='get_pc', takes_context=True)
def get_pc(context):
    """
    获取pc
    :param context:
    :return:
    """
    request = context['request']
    if request.GET.get('pc', None):
        pc = request.GET.get('pc')
    else:
        pc = 10
    context.dicts[0]['pc'] = int(pc)
    return ''


# class PageCount(template.Node):
#     def render(self, context):
#         context['pc'] = get_pc(context)
#         return ''

# register.tag('get_pc',PageCount.render)
@register.simple_tag(takes_context=True, name='make_pagination')
def make_pagination(context):
    """
    分页标签
    判断循环中的某页和当前页是否在同一分组

    :return:
    :rtype:str
    """
    """兼容方法，某些情况下只传入lines,不传入table_datas"""
    if not context.get('table_datas') and context.get('lines'):
        context['table_datas'] = context['lines']
    if len(context['table_datas']) == 0:
        return ''
    page_max, html = 10, ''
    pages = context['pages']
    request = context['request']
    # 获取当前页页码
    current_page_num = filter(lambda x: x.is_current, pages)[0].number
    # return math.ceil(page_num / page_max) == math.ceil(page_current / page_max)

    for p in pages:
        if math.ceil(p.number / page_max) == math.ceil(current_page_num / page_max):
            class_name = "active" if p.is_current else''
            html += "<li class=\"paginate_button %s\"><a href=\"%s\">%d</a></li>\n" % (class_name, p.url, p.number)
    return html


@register.simple_tag(name='show_page_data_index', takes_context=True)
def show_page_data_index(context):
    request = context['request']
    page = request.GET.get('page', default=1)
    pc = context['pc']
    index_from = (int(page) - 1) * int(pc)
    return "%s to %s " % (index_from + 1, index_from + int(pc))
