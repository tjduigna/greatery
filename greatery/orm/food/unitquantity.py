# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tortoise.models import Model
from tortoise import fields

class UnitQuantity(Model):
    id = fields.IntField(pk=True)
    unit_id = fields.ForeignKeyField('models.Unit', related_name='units')
    quantity_id = fields.ForeignKeyField('models.Quantity', related_name='quantities')

    def __str__(self):
        return f'{self.id}({self.unit_id};{self.quantity_id})'
