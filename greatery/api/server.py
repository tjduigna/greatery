#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0
import os
import json
import asyncio

from  tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application
from sprout.init_db import db_pool

import greatery
from greatery.core import Engine
from greatery.api.router import Router


def heartbeat(interval=5000, jitter=0.1):
    """Ping all live connections for debugging

    Args:
        interval (int): milliseconds between messages
        jitter (float): fuzz for simultaneous load
    """
    def _monitor():
        msg = f"Pinging {len(Router._live)} clients"
        greatery.cfg.log.info(msg)
        for id_, con in Router._live.items():
            print(id_, con)
            greatery.cfg.log.debug(id_)
            con['con'].write_message(
                json.dumps({"ping": "hello",
                            "id": str(id_)}))
    return PeriodicCallback(_monitor,
                            jitter=jitter,
                            callback_time=interval)


def run():
    opts = greatery.cfg.srv_opts
    port = opts.pop('port')
    app = Application([
        (r"/socket", Router),
    ], **opts)
    loop = asyncio.get_event_loop()
    app.engine = Engine(loop=loop)
    app.db_pool = loop.run_until_complete(db_pool('greatery'))
    srv = HTTPServer(app)
    srv.listen(port)
    opts['port'] = port
    heartbeat().start()
    IOLoop.current().start()


if __name__ == '__main__':
    run()
