#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask


def create_app(config):
    # __name__ 用于找到 static和templates的目录, 类似于os.path.dirname(os.path.abspath(模块名.__file__))
    # static 目录用来放置CSS, Javascript等静态文件, 用户可以通过HTTP协议直接访问
    # templates 目录用来存放 Jinja2 模板文件
    app = Flask(__name__, static_folder='static', template_folder='templates',)
    app.config.from_object(config)

    from .main import main as bp
    app.register_blueprint(bp, url_prefix='/')

    return app
