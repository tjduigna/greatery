# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

from tortoise.models import Model
from tortoise import fields

class Unit(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    abbr = fields.TextField()
    desc = fields.TextField()

    def __str__(self):
        return self.name
