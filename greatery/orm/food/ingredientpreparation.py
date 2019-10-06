# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tortoise.models import Model
from tortoise import fields

class IngredientPreparation(Model):
    id = fields.IntField(pk=True)
    ingredient_id = fields.ForeignKeyField('models.Ingredient', related_name='ingredients')
    preparation_id = fields.ForeignKeyField('models.Preparation', related_name='preparations')

    def __str__(self):
        return f'{self.id}({self.ingredient_id};{self.preparation_id})'
