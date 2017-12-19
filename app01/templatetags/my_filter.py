#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# 将获取到 image 的大小由Byte转换为MB，进制为1000。

from django import template

register = template.Library()


@register.filter(name='b2mb')
def convert(value):
    value = float(203538471) / 1000 / 1000

    return '%.1f %s' % (value, 'MB')
