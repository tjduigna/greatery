# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

import json
import uuid

from tornado.websocket import WebSocketHandler

import greatery
from greatery.orm.food import Ingredient
from greatery.orm.food import Recipe
from greatery.orm.food import Meal


_TOPN = 3
_CHUNK = 1000
_KEYS = {}
_TACK = {}
_TABLES = {
    'ingredient': Ingredient,
    'recipe': Recipe,
    'meal': Meal
}


class Router(WebSocketHandler, greatery._Log):
    """Core websocket handler class for greatery.
    on_message routes behavior based on the key
    in the message payload. Expects client to
    manage interactive state and provide it to
    routed methods since the "state" is driven
    by the user.
    
    Supported keys
        - route - one of the above (the verb)
        - kind - a data concept (the noun)
        - content - client message

    Supported routes
        - fetch
        - model
        - write

    Note:
        Should standardize this routing to map directly
        to CRUD or something not just made up...
    """
    _live = {}


    def open(self):
        """Keep track of all live connections"""
        self.id = str(uuid.uuid4())
        self._live[self.id] = {'id': self.id}
        msg = f"opened: {self.id}"
        self.log.info(msg)
        self.write_message(json.dumps({'id': self.id}))


    def on_close(self):
        self.log.info(f"closed: {self.id}")
        self._live.pop(self.id)


    def check_origin(self, origin):
        self.log.warning(f"ALLOWING ALL CORS: {origin}")
        return True


    async def _incref(self, route):
        """Keep count of all requests from client"""
        self._live[self.id].setdefault(route, 0)
        self._live[self.id][route] += 1


    async def on_fetch(self, kind, msg):
        """Fetches all data of a given data concept,
        optionally "caching" the greatest tack field
        in the query response, to use as a filter in
        subsequent queries to fetch data.
        """
        tbl = _TABLES.get(kind, None)
        if tbl is None:
            self.log.error("'kind' not recognized")
            return
        start = msg.get('start', 0)
        stop = start + _CHUNK
        self.log.info(f"start: {start}, stop: {stop}")
        fetch = await tbl.filter(id__gte=start, id__lte=stop)
        keys = getattr(tbl, 'ui', None)
        if not keys:
            self.log.error(f"ui keys for {tbl} not found")
            return
        ret = json.dumps(
            [{key: getattr(rec, key) for key in keys} for rec in fetch]
        )
        self.log.info(ret)
        self.write_message(ret)


    async def on_model(self, kind, msg):
        """Provided a message from the client, run
        entity recognition on the content and serve
        back the most closely matching data currently
        in the dataset.
        """
        self.log.info("hit model")
        eng = self.application.engine
        self.log.info(f"model target '{msg['content']}'")
        model = eng.onion._graph_models.get(kind, None)
        if model is None:
            self.log.error(f"found no '{kind}' model")
            return
        if isinstance(msg['content'], str):
            pred = model.predict([msg['content']])
        elif isinstance(msg['content'], dict):
            self.log.warn("poor support for dicts right now")
            pred = model.predict([' '.join(msg['content'].values())])
        else:
            self.log.error(f"support msg content type {type(msg['content'])}!")
        ret = json.dumps(
            pred.iloc[:_TOPN].to_dict(orient='records')
        )
        self.write_message(ret)


    async def on_write(self, kind, msg):
        """Write a new record of data to a specific
        data concept's database table. Requires the
        specification of 'table', 'keys', as well as
        'tack' in order to persist data (right now).
        """
        self.log.info("hit write")
        self.log.info(msg)
        tbl = _TABLES.get(kind, None)
        self.log.info(tbl)
        if tbl is None:
            self.log.error(f"{kind} not recognized")
            return
        pk = getattr(tbl, 'pk', None)
        self.log.info(pk)
        if pk is None:
            self.log.error(f"pk not defined for {tbl}")
            return
        ui = getattr(tbl, 'ui', None)
        self.log.info(ui)
        if ui is None:
            self.log.error(f"keys not defined for {tbl}")
            return
        keys = [k for k in ui if k != pk]
        self.log.info(keys)
        kws = {'name': msg['content']}
        self.log.info(kws)
        rec = await tbl.create(**kws)
        self.log.info(rec)
        await rec.save()


    async def on_message(self, msg):
        """Route incoming websocket message to
        appropriate handler.
        """
        msg = json.loads(msg)
        kind = msg.get('kind', None)
        route = msg.get('route', None)
        await self._incref(route)
        self.log.info(self._live[self.id])
        print(msg)
        if kind is None:
            self.log.error("'kind' not provided")
            return
        if route is None:
            self.log.error("'route' not provided")
            return
        if route == 'fetch':
            await self.on_fetch(kind, msg)
        elif route == 'model':
            await self.on_model(kind, msg)
        elif route == 'write':
            await self.on_write(kind, msg)
        else:
            self.log.error(f"kind='{kind}' not recognized")
