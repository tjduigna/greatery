# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tortoise.models import Model
from tortoise import fields

class Quantity(Model):
    id = fields.IntField(pk=True)
    amount = fields.DecimalField(max_digits=38, decimal_places=12)
    unit = fields.ForeignKeyField('models.Unit', related_name='units')

    def __str__(self):
        return f'{self.name}({self.amount};{self.unit})'
