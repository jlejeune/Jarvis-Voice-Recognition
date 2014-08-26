# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import os

from jarvis.flask.models import init_databases


def configure_db(options):
    # Test if basedir folder exists
    if not os.path.exists(options.basedir):
        os.makedirs(options.basedir)

    # Test if db is initialized
    if not os.listdir(options.basedir):
        init_databases()
