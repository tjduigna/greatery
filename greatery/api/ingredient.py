# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tornado.web import RequestHandler

from greatery.orm.food import Ingredient


ingredients = []

class IngredientHandler(RequestHandler):

    async def get(self):
        got = 0
        if ingredients:
            got = max(obj.get('id', 0) for obj in ingredients) + 1
        ings = await Ingredient.filter(id__gte=got)
        ingredients.extend([{'name': obj.name,
                             'desc': obj.desc,
                             'id': obj.id} for obj in ings])
        self.redirect('/')

    async def post(self):
        ing = await Ingredient.create(
            name=self.get_argument('name').upper(),
            desc=self.get_argument('desc').upper()
        )
        if ing.name:
            await ing.save()
        else:
            print("no name provided.")
        self.redirect('/')
