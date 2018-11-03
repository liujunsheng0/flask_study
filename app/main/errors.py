#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return '404, %s' % str(e), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return '500, %s' % str(e), 500
