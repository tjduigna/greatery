#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

import asyncio
import websockets

import greatery


async def hello(websocket, path):
    print("hello", websocket, path)
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

opts = greatery.cfg.ws_opts

start_server = websockets.serve(
    hello, opts['host'], opts['port'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
