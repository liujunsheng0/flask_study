#!/usr/bin/python3
# -*- coding: utf-8 -*-


import time
def application(env: dict, start_response):
    """
    这样的写法为了与wsgi的写法保持一致, 可以自定义输入和输出
    :param env: dict
    :param start_response: 回调函数
    :return: response body
    """

    _, status = env, "200 OK"
    server_headers = [("server", "pycharm server")]
    # #这也是很重要的一步，返回服务器函数
    start_response(status, server_headers)
    return time.ctime()
