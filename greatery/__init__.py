# -*- coding: utf-8 -*-
# Copyright 2019, Greatery Development Team
# Distributed under the terms of the Apache License 2.0

import os
import yaml
import getpass
import logging.config


_home = os.path.expanduser('~')
_root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_root, 'conf', 'log.yml'), 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))
_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


class _Log:
    @property
    def log(self):
        return logging.getLogger(
            '.'.join([
                self.__module__,
                self.__class__.__name__
            ])
        )


class cfg(_Log):

    def _load_cfg_fl(self, *path_parts, root=_root, cache=True):
        fp = os.path.join(root, *path_parts)
        r = {}
        if cache:
            r = self._cfg.get(fp, {})
            if r:
                return r
        try:
            with open(fp, 'r') as f:
                r = yaml.safe_load(f.read())
        except FileNotFoundError as e:
            self.log.error(f"file not found: {fp}")
        if cache:
            self._cfg[fp] = r
        return r

    @property
    def environment(self):
        if self._environment is None:
            self._environment = os.environ.get('ENVIRONMENT', 'local')
        return self._environment

    @property
    def ws_opts(self):
        if self._ws_opts is None:
            opts = self._load_cfg_fl('conf', 'ws.yml')
            self._ws_opts = opts[self.environment]
        return self._ws_opts

    @property
    def srv_opts(self):
        if self._srv_opts is None:
            opts = self._load_cfg_fl('conf', 'srv.yml')
            self._srv_opts = opts[self.environment]
        return self._srv_opts

    @property
    def db_opts(self):
        if self._db_opts is None:
            opts = self._load_cfg_fl('conf', 'db.yml')
            rc = {}
            try:
                rc = self._load_cfg_fl('.greateryrc', root=_home)
            except FileNotFoundError:
                self.log.error("no ~/.greateryrc found")
            self._db_opts = opts[self.environment]
            self._db_opts.update(rc)
        return self._db_opts

    def db_str(self, dbname=None, schema=None):
        o = self.db_opts
        dbname = dbname or o['database']
        auth = f"{o['username']}:{o['password']}"
        url = f"{o['host']}:{o['port']}"
        if schema is not None:
            return f"{o['driver']}://{auth}@{url}/{dbname}?schema={schema}"
        return f"{o['driver']}://{auth}@{url}/{dbname}"

    def reset(self):
        self._cfg = {}
        self._ws_opts = None
        self._db_opts = None
        self._srv_opts = None
        self._environment = None

    def __init__(self):
        self.reset()

cfg = cfg()


from greatery import core
