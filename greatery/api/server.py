#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0
import os
import asyncio
from functools import partial

from  tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.web

from react.render import render_component

import greatery
from greatery.orm.init_db import init_db, db_pool
from greatery.api.ingredient import IngredientHandler, ingredients


_here = partial(os.path.join, greatery._root, '..', 'js')

kinds_of_entries = [
    {'value': 'chocolate', 'label': 'Chocolate'},
    {'value': 'strawberry', 'label': 'Strawberry'},
    {'value': 'vanilla', 'label': 'Vanilla'}
]

real_entries = [
    {'value': 'ingredients', 'label': 'Ingredients'},
    {'value': 'preparations', 'label': 'Preparations'},
    {'value': 'quantities', 'label': 'Quantities'},
    {'value': 'units', 'label': 'Units'},
    {'value': 'meals', 'label': 'Meals'},
]


class IndexHandler(tornado.web.RequestHandler):

    async def get(self):
        rendered = render_component(
            _here('src', 'app.jsx'), {
                'entries': ingredients,
                'url': '/ingredients',
                'kinds_of_entries': kinds_of_entries,
                'xsrf': self.xsrf_token.decode('ascii')
            }, to_static_markup=False)
        self.render('index.html',
                    title='Greatery',
                    rendered=rendered)



def main():
    stg = {
        'template_path': _here('templates'),
        'static_path': _here('static'),
        'cookie_secret': os.urandom(12),
        'xsrf_cookies': True,
        'debug': True,
        'autoreload': True,
        'compress_response': True
    }
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/ingredients", IngredientHandler),
    ], **stg)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    app.db_pool = loop.run_until_complete(db_pool())
    srv = HTTPServer(app)
    srv.listen(greatery.cfg.srv_opts['port'])
    IOLoop.current().start()


if __name__ == '__main__':
    main()
