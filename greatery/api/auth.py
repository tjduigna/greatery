# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

import json
import asyncio

from tornado.web import RequestHandler

import greatery


class LoginHandler(RequestHandler):

    def set_default_headers(self):
        print("setting headers")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Request-Headers",
                        "Origin, Content-Type, Accept")
        self.set_header("Access-Control-Allow-Methods",
                        "GET,PUT,POST,DELETE,PATCH,OPTIONS")

    async def get(self):
        print("get", self.request)

    async def post(self):
        req = json.loads(self.request.body)
        for key in ['username', 'password']:
            assert key in req
        print(req)


    async def options(self):
        print("options", self.request)
        self.set_status(204)
        self.finish()
