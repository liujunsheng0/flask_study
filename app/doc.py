#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask import (redirect, abort, url_for, make_response, request, g)
from werkzeug.local import Local, LocalStack, LocalProxy

"""
视图函数的返回值会自动转换为一个响应对象, 如果返回值是
    1. 响应对象, 直接返回它
    2. 字符串, 会被转换为一个包含作为响应体的字符串,一个 200 OK 出错代码 和一个 text/html 类型的响应对象
    3. 元组, 那么元组中的项目可以提供额外的信息,元组中必须至少 包含一个项目,且项目应当由 (response, status, headers)
       或者 (response, headers) 组成, status 的值会重载状态代码, headers 是一个由额外头部值组成的列表或字典,
    4. 如果以上都不是,那么 Flask 会假定返回值是一个有效的 WSGI 应用并把它转换为 一个响应对象
    5. 如果想要在视图内部掌控响应对象的结果, 则可以使用 flask.make_response()

url_for  利用endpoint, 构建指定视图的url; endpoint一般为函数名
redirect 重定向
abort    更早的退出请求
"""

a = 1
b = 2
print(exec('c=a+b'))
print(c)

