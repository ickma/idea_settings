# coding:utf8
# @author:nick
# @company:joyme

from . import register


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


@register.filter(name='create_show_index')
def create_show_index(datas):
    """
    生成用于显示的id
    将数据库中的id进行重新排序
    :param datas:
    :type datas:list
    :return:
    """
    data_length = len(datas)
    for k, line in enumerate(datas):
        line.show_index = data_length - k

    return datas


@register.filter(name="create_choose_html")
def create_choose_html(instance):
    """

    :param instance:
    :return:
    """
    return """
      <td data-delete-id="{0}"><input type="checkbox" title=""></td>
    """.format(instance.id)
