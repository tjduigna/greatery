# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

import json
import asyncio

from tornado.web import RequestHandler

import greatery


class LoginHandler(RequestHandler):

    def set_default_headers(self):
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
        #print("json loaded request")
        user = req.get('username', None)
        pw = req.get('password', None)
        #print(req)
        #print(user, pw)
        if not user or not pw:
            #print("request fkd")
            self.write({"error": "malformed request"})
            self.set_status(407)
            self.finish()
            return
        if user != 'greatery-admin' or pw != 'supersecret':
            #print("request unauthorized")
            self.write({"error": "authentication denied"})
            self.set_status(403)
            self.finish()
            return
        #print("Made it past all the checks")
        self.write(json.dumps({"authorized": True}))
        self.set_status(200)

    async def options(self):
        #print("options", self.request)
        self.set_status(204)
        self.finish()
