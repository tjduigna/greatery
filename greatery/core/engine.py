# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0
import asyncio

import pandas as pd
import onion
from sprout import Runner

import greatery
from greatery.orm.food import (
    Unit,
    Quantity,
    Ingredient,
    Recipe,
    Meal,
)

# TODO : _schemas is obj.graph

_schemas = {
    'food': {
#        'unit': Unit,
#        'quantity': Quantity,
        'ingredient': Ingredient,
        'recipe': Recipe,
        'meal': Meal,
    }
}


class Engine:
    """The interface between the database schema
    and the onion model. Intended to fuel smart
    completion and recognition with a web app.
    """

    async def fetchall(self, graph):
        """Get all the data (for now)
        
        Args:
            graph (dict): {schema: [tables]}

        Returns:
            graph updated with data
        """
        data = {}
        for schema, rel in graph.items():
            sub = _schemas[schema]
            for name in rel:
                dat = await sub[name].all()
                if not dat: continue
                keys = [k for k in vars(dat[0]).keys()
                        if not k.startswith('_') and k != 'id']
                data[name] = pd.DataFrame.from_records(
                    ({k: getattr(d, k) for k in keys} for d in dat)
                )
        graph.update(data)
        return graph

    def __init__(self, runner=None):
        graph = {
            'food': [
                'ingredient',
                'recipe',
                'meal',
            ]
        }
        self.runner = runner or Runner(greatery.cfg.db_opts,
                                       app='greatery',
                                       schemas=['food'])
        self.runner.init_schemas()
        graph = self.runner._loop.run_until_complete(self.fetchall(graph))
        self.onion = onion.Onion('food', graph, None)
