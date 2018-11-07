#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from flask_script import Manager
from app import create_app
from config import get_config


app_ = create_app(get_config())
manager = Manager(app_)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        app_.run(debug=True)
    else:
        manager.run()
