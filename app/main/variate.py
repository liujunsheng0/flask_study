#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import main

# 转换器类型
# string   缺省值, 接受任何不包含斜杠的文本
# path	   可以包含斜杠(/)的字符串
# int	   接受正整数, float类型是调用不到该视图的
# float	   接受正浮点数
# uuid	   接受 UUID 字符串


# http://127.0.0.1:5000/user/jim/1111      ok
# http://127.0.0.1:5000/user/jim/1111.00   not found
@main.route('/user/<user>/<int:age>')
def show_variate(user: str, age: int):
    return 'User %s, Age= %s' % (user, age)


@main.route('/path/<path:sub_path>')
def show_path(sub_path):
    return 'sub path %s' % sub_path
