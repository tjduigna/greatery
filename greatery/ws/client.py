#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

import asyncio
import websockets

import greatery


async def hello():
    opts = greatery.cfg.ws_opts
    uri = f"ws://{opts['host']}:{opts['port']}"

    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
