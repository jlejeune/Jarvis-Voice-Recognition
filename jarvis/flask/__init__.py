#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from __version__ import version
except ImportError:
    version = "unknown"

import os
from flask import Flask

from jarvis.tools.daemon import WSGIDaemon
from jarvis.tools.config import JarvisServerConfig


def parse_options():
    parser = JarvisServerConfig(usage='%prog [options]',
                                version=version,
                                name="jarvis-server",
                                description="Jarvis Server")
    parser.add_options_server()

    (args, actions) = parser.parse_args()

    parser.check_options_server(WSGIDaemon, args)

    return (args, actions)

# Configure app
(options, actions) = parse_options()
application = Flask(__name__)

# Update application config with options
application.config.update(vars(options))

# Update application config from file
if not application.config.get('API_LOGGING'):
    # Try to check if the local configuration is present (in the source)
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    local_config_path = os.path.join(root_path, 'defaults.cfg')
    if os.path.isfile(local_config_path):
        application.config.from_pyfile(local_config_path, silent=True)

# Register modules
from jarvis.flask.views.epg import epg
from jarvis.flask.views.tts import tts
from jarvis.flask.views.traffic import traffic
application.register_blueprint(epg)
application.register_blueprint(tts)
application.register_blueprint(traffic)
