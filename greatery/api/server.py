#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0
import os
import json
import asyncio

from  tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from sprout.init_db import db_pool

import greatery
from greatery.core import Engine
from greatery.api.router import Router


def run():
    stg = {
        'cookie_secret': os.urandom(12),
        'xsrf_cookies': True,
        'debug': True,
        'autoreload': True,
        'compress_response': True
    }
    app = Application([
        (r"/socket", Router),
    ], **stg)
    loop = asyncio.get_event_loop()
    app.engine = Engine(loop=loop)
    app.db_pool = loop.run_until_complete(db_pool('greatery'))
    srv = HTTPServer(app)
    srv.listen(greatery.cfg.srv_opts['port'])
    IOLoop.current().start()


if __name__ == '__main__':
    run()
