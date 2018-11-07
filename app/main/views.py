#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import (render_template)

from . import main


# route 装饰器将函数绑定到 url; endpoint默认为函数名; methods,允许的访问方式, 默认为GET
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')