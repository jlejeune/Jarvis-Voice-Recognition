
try:
  from __version__ import version
except ImportError:
  version = "unknown"

from flask import Flask
from jarvis.tools.daemon import WSGIDaemon
from jarvis.tools.config import JarvisServerConfig

def parse_options():

    parser = JarvisServerConfig(usage = '%prog [options]',
                                version=version,
                                name = "jarvis-server",
                                description = 'Jarvis Server')
    parser.add_options_server()

    (args, actions) =  parser.parse_args()

    parser.check_options_server(WSGIDaemon, args, actions)

    return (args, actions)

# Configure app
(options, actions) = parse_options()
application = Flask(__name__)

# Update application config with options
application.config.update(vars(options))

# Register modules
from jarvis.flask.views import epg
application.register_blueprint(epg)
