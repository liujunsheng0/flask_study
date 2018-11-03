#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
基于已经实现的WSGI模块 使用wsgi
WSGI(web server gateway interface): Web服务器网关接口
http://mingxinglai.com/cn/2016/08/flask-source-code/#top
https://segmentfault.com/a/1190000003069785
"""


import os
from eventlet import wsgi, listen


"""
web server: 请求入口, 只能接受外界的请求并调用下一段管件的函数
middleware: 中间的管件(中间件), 既可以接收上一段管件的请求, 又可以调用下一段管件的函数(可以有多个)
web app: 管道的终点, 只能被上一段管件调用

WSGI: 一个规范, 定义了Web服务器如何与Python应用程序进行交互, 使得Python的Web应用程序可以和Web服务器对接起来
      WSGI相当于Web服务器和Python应用程序之间的桥梁

出现WSGI的原因: 定义Web服务器和应用程序之间的交互

WSGI的用处:
    让Web服务器知道如何调用Python应用程序, 并且把用户的请求告诉应用程序
    让Python应用程序知道用户的具体请求是什么, 以及如何返回结果给Web服务器

WSGI协议主要包括server和application(应用)两部分:
    WSGI server: 负责从客户端接收请求, 将request转发给application, 将application返回的response返回给客户端;
                 可以认为WSGI server就是一个web server
    WSGI application: 接收由server转发的request, 处理请求, 并将处理结果(response)返回给server.
         application中可以包括多个栈式的中间件(middleware), 这些中间件需要同时实现server与application,
         因此可以在WSGI服务器与WSGI应用之间起调节作用, 对服务器来说, 中间件扮演应用程序, 对应用程序来说, 中间件扮演服务器
    WSGI协议其实是定义了一种server与application解耦的规范, 即可以有多个实现WSGI server的服务器, 也可以有多个实现
    WSGI application的框架, 那么就可以选择任意的server和application组合实现自己的web应用

WSGI定义了application对象的形式:
    def simple_app(environ, start_response):
        pass

    environ: dict, 存放了所有和客户端相关的信息
             environ包含: CGI规范要求的数据
                          WSGI规范新增的数据
                          操作系统的环境变量
                          sWeb服务器相关的环境变量

    start_response: 响应函数, 一个可调用对象, 接收两个必选参数和一个可选参数, 返回值用于为HTTP响应提供body
             status: str, 表示HTTP响应状态字符串
             response_headers: list, 包含有如下形式的元组: (header_name, header_value), 用来表示HTTP响应的headers
             exc_info(可选): 用于出错时, server返回给浏览器的信息

Flask, Django 就是运行在WSGI上的web框架
实现了WSGI的模块有wsgiref(python内置), werkzeug.serving, twisted.web等
"""

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def app(environ: dict, start_response):
    """
    直接使用库 WSGI
    """
    start_response('200 OK', [('Content-Type', 'text/plain')])

    # for k, v in environ.items():
    #     print(k, v)

    # 通过Werkzeug, 可以不必直接处理请求或者响应这些底层的东西, 已经处理好了
    uri = environ.get('PATH_INFO', '')

    if uri == '/favicon.ico':
        return ''

    if uri in ('/index', '/'):
        path = os.path.join(data_dir, 'index.html')
    else:
        path = os.path.join(data_dir, uri.lstrip('/'))
    if os.path.exists(path):
        return read_file(path)
    else:
        return 'filename=%s not found!!!' % uri.lstrip('/')


if __name__ == '__main__':
    wsgi.server(listen(('0.0.0.0', 8000)), app)
