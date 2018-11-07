#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from datetime import timedelta


class Config(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)


class DevConfig(Config):
    ENV = 'develop'


class TestConfig(Config):
    ENV = 'test'


class OnlineConfig(Config):
    ENV = 'online'


_config = {'test': TestConfig, 'develop': DevConfig, 'online': OnlineConfig, 'dev': DevConfig}


def get_config():
    mode = os.environ.get('MODE', '').lower()
    config = _config.get(mode, DevConfig)
    print('mode = %s' % config.ENV)
    return config


if __name__ == '__main__':
    get_config()
