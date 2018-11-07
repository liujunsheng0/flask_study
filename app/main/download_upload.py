#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

from flask import (jsonify, request, make_response, send_file, url_for, redirect)
from werkzeug.utils import secure_filename

from . import main


@main.route('/download', methods=['GET', 'POST'])
def download():
    path = request.args.get('path', "")
    # 存在安全隐患...
    if not path or not os.path.exists(path):
        return jsonify({'msg': '%s not exist' % path})
    response = make_response(send_file(path, as_attachment=False))
    # http://gresstant.com/?p=78, flask框架问题, 发送中文bug
    # https://stackoverflow.com/questions/47575665/flask-raises-unicodeencodeerror-latin-1-when-send-attachment-with-utf-8-charac
    if not re.findall(r'[\u4e00-\u9fa5]+', path):
        response.headers["Content-Disposition"] = "attachment; filename=%s;" % os.path.basename(path)
    return response


@main.route('/upload', methods=['POST'])
def upload():
    upload_dir = os.path.join(main.static_folder, 'upload')
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    for k in request.files:
        f = request.files.get(k)
        if f:
            filename = secure_filename(f.filename)
            upload_path = os.path.join(upload_dir, filename)
            f.save(upload_path)
    return 'upload file success'


# 访问static下的文件
# 可使用url_for('static', filename='xxx')的方式访问static下的文件
@main.route('/static_img')
def static_img():
    # http://127.0.0.1:5000/static/imgs/favicon.ico, 自己在浏览器直接访问该网址也是可以的
    # 如果是pdf文件是在线浏览的.
    # redirect: 重定向
    return redirect(url_for('static', filename='imgs/favicon.ico'))
