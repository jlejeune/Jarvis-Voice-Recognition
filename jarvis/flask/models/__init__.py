# -*- coding: utf-8 -*-
#!/usr/bin/python
# vim:set ai et sts=4 sw=4:

from epg import Epg
from sqlite3 import OperationalError


def init_databases():
    try:
        # Init Epg database and tables
        Epg.create_table()
    except OperationalError, err:
        print err
