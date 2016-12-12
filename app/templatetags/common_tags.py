# coding:utf8
# @author:nick
# @company:joyme
from django import template
from permissions.models.log_model import WebRequest
from app.menu_settings import MENU_CONFIG

# 网站统计tags
register = template.Library()


@register.simple_tag(name='visit_count')
def visit_count():
    return WebRequest.objects.count() + 1


@register.simple_tag(name='copy_right')
def copy_right_html():
    return """
     <strong>Copyright &copy; 2016 <a href="http://www.heyijoy.com/">HEYI JOYME</a>.</strong> All rights reserved.
    """


def get_side_bar():
    for m in MENU_CONFIG:
        li_html = ''
        for c in m.children:
            li_html += '<li><a href="{href}">{c_name}</a></li>'.format(href=c.path, c_name=c.name)
        html = """
        <li class="treeview">
        <a href="#">
        <i class="fa fa-link"></i>
        <span>{m_name}</span>
        <span class="pull-right-container">
              <i class="fa fa-angle-left pull-right"></i>
            </span>
            <ul class="treeview-menu menu-open" style="display: block;">
                     {li_tml}
                    </ul>
        """.format(m_name=m.name, li_html=li_html)
        return html
