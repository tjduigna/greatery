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


_TOP_N = 3
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
    in the message payload. 
    
    Note: Supported routes
        - fetch
        - model
        - write

    Note: Supported keys
        - route - one of the above
        - kind - a data concept
        - content - client message
    """
    table = None
    model = None
    keys = ['id', 'name', 'desc']
    tack = 'id'
    _live = {}

    def tbl_fields(self):
        """Return a list of the relevant fields
        for a given data concept."""
        if self.keys is not None:
            return self.keys
        if self.table is not None:
            flds = vars(self.table).keys()
            return [key for key in flds
                    if not key.startswith('_')]
        return []

    def open(self):
        """Keep track of all live connections"""
        self.id = uuid.uuid4()
        self._live[self.id] = {'id': self.id}
        self.log.info(f"opened: {self.id}")

    async def on_fetch(self, msg):
        """Fetches all data of a given data concept,
        optionally "caching" the greatest tack field
        in the query response, to use as a filter in
        subsequent queries to fetch data.
        """
        if self.table is None:
            self.log.error(f"no table to fetch")
            return
        self.log.debug(f"on_fetch: {msg}")
        start = self._live[self.id].get('start', 0)
        self.log.info(f"fetch start {start}")
        fetch = await self.table.filter(id__gte=start)
        keys = self.tbl_fields()
        self.log.info(f"fetch keys {keys}")
        resp = [{key: getattr(rec, key) for key in keys}
                for rec in fetch]
        self.log.info(f"fetch count {len(resp)}")
        if self.tack is None:
            self.log.warning(f"not caching table read")
        else:
            start = max((r[self.tack] for r in resp))
            self._live[self.id]['start'] = start
        self.write_message(json.dumps(resp))

    async def on_model(self, msg):
        """Provided a message from the client, run
        entity recognition on the content and serve
        back the most closely matching data currently
        in the dataset.
        """
        if self.model is None:
            self.log.error(f"no model to predict")
            return
        self.log.debug(f"on_model: {msg}")
        eng = self.application.engine
        self.log.info(f"model target {msg}")
        model = eng.onion._graph_models[self.model]
        self.log.info(f"model space {len(model.tokens)}")
        resp = model.predict([msg]
            ).iloc[:_TOP_N].to_dict(orient='records')
        self.log.info(f"model top {resp['name']}")
        self.write_message(json.dumps(resp))

    async def on_write(self, msg):
        """Write a new record of data to a specific
        data concept's database table. Requires the
        specification of 'table', 'keys', as well as
        'tack' in order to persist data (right now).
        """
        for attr in ['table', 'keys', 'tack']:
            if getattr(self, attr) is None:
                self.log.error(f"no {attr} for write. aborting")
                return
        self.log.debug(f"on_write: {msg}")
        kws = {key: msg[key] for key in
               [key for key in self.keys if key != self.tack]}
        rec = await self.table.create(**kws)
        self.log.info(f"adding record {msg}")
        if rec.name:
            self.log.info(f"record name |{name}|")
            await ing.save()

    async def on_message(self, message):
        """Route incoming websocket message to
        appropriate handler.
        """
        message = json.loads(message)
        kind = message['kind']
        route = message['route']
        content = message['content']
        self.log.debug(f"routing {kind} {route} with {content}")
        self.model = kind
        self.table = _TABLES[kind]
        self.keys = _KEYS.get(kind, self.keys)
        self.tack = _TACK.get(kind, self.tack)
        await {
            'fetch': self.on_fetch,
            'model': self.on_model,
            'write': self.on_write,
        }[route](content)
        self.set_header("Content-Type",
                        "application/json")

    def on_close(self):
        self._live.pop(self.id)
        self.log.info(f"closed: {self.id}")

    def check_origin(self, origin):
        self.log.warning(f"ALLOWING ALL CORS")
        return True
