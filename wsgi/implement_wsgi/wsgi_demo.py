#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import re
from socket import socket, AF_INET, SOCK_STREAM
from copy import deepcopy
from threading import Thread


data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


# 可调用对象是一个函数
def app(environ, start_response):
    uri = environ.get('uri', '')
    if uri in ('/', '', '/index'):
        path = os.path.join(data_dir, 'index.html')
    else:
        path = os.path.join(data_dir, uri.lstrip('/'))
    status = '200 OK'
    if os.path.exists(path):
        response_body = read_file(path)
    else:
        status = '404 OK'
        response_body = 'filename=%s is not found!!!' % uri.lstrip('/')

    # 应答的头部是一个列表，每对键值都必须是一个 tuple。
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]
    # 调用服务器程序提供的 start_response，填入两个参数
    start_response(status, response_headers)
    print('response_body:', response_body)
    return response_body


# 中间件, 将env中 所有类型为str的值全部转变为大写
def app_wrapper(app_func):
    def wrapper(*args, **kwargs):
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                if isinstance(v, str):
                    args[0][k] = v.upper()
        return app_func(*args, **kwargs)
    return wrapper


class WSGI(object):
    def __init__(self, app_, host="127.0.0.1", port=8000):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.app = app_
        self.response_header = ''

        # 环境变量
        environ = dict(os.environ.items())
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = True
        environ['wsgi.run_once'] = True
        environ['wsgi.url_scheme'] = 'http'
        self.environ = environ
        self.response_header = ''

    def run(self):
        while True:
            print('waiting......')
            client, ip_port = self.server.accept()
            ip, port = ip_port
            print('connecting %s:%s' % (ip, port))
            Thread(target=self._handler, args=(client, )).run()

    def start_response(self, status, response_headers, exc_info=None):
        _ = exc_info
        response_header = "HTTP/1.1 " + status + "\r\n"
        for header in response_headers:
            response_header += "%s:%s\r\n" % header
        self.response_header = response_header

    def _handler(self, client):
        receive = client.recv(1024)
        receive_lines = receive.splitlines()
        # 解析http报文, 此处省略, 只解析了uri
        uri = ''
        if receive_lines:
            uri = re.match(r"\w+ +(/[^ ]*) ", receive_lines[0].decode("utf-8")).group(1)
        environ = deepcopy(self.environ)
        environ['uri'] = uri
        response_start_line = ''
        try:
            response_body = self.app(environ, self.start_response)
        except Exception as e:
            print(e)
            response_start_line = "HTTP/1.1 404 error\r\n"
            response_body = str(e)

        response_headers = self.response_header
        response = response_start_line + response_headers + "\r\n" + response_body
        self.response_header = ''

        print("\nresponse data start \n", response, '\nresponse data end\n')
        client.send(response.encode("utf-8"))
        client.close()


if __name__ == '__main__':
    # demo, 单线程
    WSGI(app).run()
    # WSGI(app_wrapper(app)).run()
