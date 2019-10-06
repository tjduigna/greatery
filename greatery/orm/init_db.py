# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

import asyncio
import asyncpg
from tortoise import Tortoise

import greatery
from greatery.orm import *


async def _create_database(base, name):
    con = await asyncpg.connect(base)
    try:
        await con.execute(f"create database {name};")
    except asyncpg.exceptions.DuplicateDatabaseError:
        greatery.cfg.log.info(f"database {name} exists")
    finally:
        await con.close()

async def _create_schema(base, name):
    con = await asyncpg.connect(base)
    try:
        await con.execute(f"create schema {name};")
    except asyncpg.exceptions.DuplicateSchemaError:
        greatery.cfg.log.info(f"schema {name} exists")
    finally:
        await con.close()

async def init_db(dbname='greatery'):
    base = greatery.cfg.db_str()
    await _create_database(base, dbname)
    base = greatery.cfg.db_str(dbname)
    for schema in ['food']:
        await _create_schema(base, schema)
        await Tortoise.init(
            db_url=greatery.cfg.db_str(dbname, schema),
            modules={'models': [f'greatery.orm.{schema}']}
        )
        await Tortoise.generate_schemas()
        greatery.cfg.log.info(f"{schema} ready")

async def db_pool(dbname='greatery'):
    opts = greatery.cfg.db_opts.copy()
    opts['database'] = dbname
    opts['user'] = opts.pop('username')
    opts.pop('driver')
    pw = opts.pop('password')
    greatery.cfg.log.debug('asyncpg pool init')
    greatery.cfg.log.debug(opts)
    opts['password'] = pw
    pool = await asyncpg.create_pool(**opts)
    return pool


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
