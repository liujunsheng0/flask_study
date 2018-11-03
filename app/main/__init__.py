#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Blueprint

# main 放前面是因为 views和errors依赖了main
# 蓝图的 name 不能相同, 保证唯一性
main = Blueprint('main', __name__)

from . import errors
from . import views
