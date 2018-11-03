#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://zhuanlan.zhihu.com/p/33551007

服务器可以返回静态的网页, 但是还是不能满足需求, 网页数据都是变化的.
于是就有了WSGI协议(Web Server Gateway Interface), 想让网页数据随时变化, 就需要引入可执行的代码,
WSGI协议就提供了这样一个接口, 可以根据客户端的请求, 调用py文件.

http://127.0.0.1:8000/app.py  -> 调用app.py中的函数, 返回当前时间
http://127.0.0.1:8000/        —> 读取index.html
http://127.0.0.1:8000/1.txt   —> 读取1.txt
http://127.0.0.1:8000/no      —> 直接返回浏览器无法解析的http报文

试试POST请求, 看下原始报文

"""

import os
import re
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM


class Socket(object):
    """ socket 监听端口, 自己解析http协议 """
    def __init__(self, host="127.0.0.1", port=8000):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)

        self.response_header = ''
        self.dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

    def run(self):
        while True:
            print('waiting......')
            client, ip_port = self.server.accept()
            ip, port = ip_port
            print('connecting %s:%s' % (ip, port))
            t = Thread(target=self._handle, args=(client,))
            t.start()

    def start_response(self, status, server_headers):
        """ 提供给 app 使用的回调函数 """
        response_header = "HTTP/1.1 " + status + "\r\n"
        for header in server_headers:
            response_header += "%s:%s\r\n" % header
        self.response_header = response_header

    def _handle(self, client_socket):
        receive = client_socket.recv(1024)
        # 打印完整的http请求报文
        print("request data start \n", receive, '\nrequest data end\n')

        receive_lines = receive.splitlines()
        for i in receive_lines:
            print(i)

        # 解析报文中的uri (需要自己解析http协议, --!)
        uri = ''
        if receive_lines:
            uri = re.match(r"\w+ +(/[^ ]*) ", receive_lines[0].decode("utf-8")).group(1)
        print('uri =', uri)

        if uri == '/no':
            # 浏览器无法解析报文, 所以浏览器处会报如下错误
            # 该网页无法正常运作
            # 127.0.0.1 发送的响应无效。
            # ERR_INVALID_HTTP_RESPONSE
            response = 'no status, no header, no body'

        elif uri.endswith(".py") and os.path.exists(uri.lstrip('/')):
            # 导入 Python 文件, 相当于 import uri (不要.py)
            m = __import__(uri[1:-3])
            # print('m: ', m)
            env = {}
            # 调用导入模块的 application 函数, 获取application()函数的结果
            response_body = m.application(env, self.start_response)
            # 动态文件的响应报文
            response = self.response_header + "\r\n" + response_body

        else:
            if not uri or "/" == uri:
                uri = "index.html"
            path = os.path.join(self.dir, uri.lstrip('/'))
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, 'rb') as f:
                    file_content = f.read()
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_body = file_content.decode("utf-8")
            else:
                response_start_line = "HTTP/1.1 404 Not Found\r\n"
                response_body = "filename=%s is not found!" % uri.lstrip('/')
            # end if
            response_headers = "Server: pycharm server\r\n"
            response = response_start_line + response_headers + "\r\n" + response_body
        # end if

        print("\nresponse data start \n", response, '\nresponse data end\n')
        client_socket.send(response.encode("utf-8"))
        client_socket.close()


if __name__ == '__main__':
    Socket().run()
