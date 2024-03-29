# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tortoise.models import Model
from tortoise import fields

class Ingredient(Model):
    pk = 'id'
    ui = ['id', 'name', 'desc']
    id = fields.IntField(pk=True)
    name = fields.TextField()
    desc = fields.TextField()
    quantity = fields.ManyToManyField('models.Quantity', related_name='quantitys')

    def __str__(self):
        return f"{self.name}:{self.desc[:30]}"
