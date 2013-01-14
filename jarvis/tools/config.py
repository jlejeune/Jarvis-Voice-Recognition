# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import ConfigParser, optparse

options = None

# Callbacks definition
def list_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

###############################################################################
#
# Small class to parse configuration file and handle some options from the
# command line
class JarvisServerConfig(optparse.OptionParser):

    def __init__(self, *args, **kwargs):
        self.module_name = kwargs.pop('name')
        assert self.module_name
        optparse.OptionParser.__init__(self, *args, **kwargs)
        self.__add_default_options()

    def __add_default_options(self):
        self.add_option("-C",
                        "--config",
                        dest="config_file",
                        help="read configuration from FILE",
                        default="/etc/jarvis-server/jarvis-server.conf",
                        metavar="FILE")

        self.add_option("-v",
                        "--verbose",
                        action="count",
                        dest="verbose")

        self.add_option("-q",
                        "--quiet",
                        action="store_false",
                        dest="verbose",
                        help="don't print status messages to stdout")

    def add_options_client(self):
        """ Default option when connecting a client to the webservice """
        group = optparse.OptionGroup(self, "Server options")

        group.add_option("-p",
                         "--port",
                         dest="port",
                         type="int",
                         help="Set port to connect (default: %default)",
                         default=9090)

        group.add_option("-s",
                         "--server",
                         dest="server",
                         type="string",
                         help="Set address to connect (default: %default)",
                         default="127.0.0.1")

        group.add_option("-u",
                         "--user",
                         dest="user",
                         type="string",
                         metavar="<user[:password]>",
                         help="Set server user and password",
                         default=None)

        self.add_option_group(group)

    def add_options_server(self):
        """ Default option when launching a webserver """
        group = optparse.OptionGroup(self, "Server options")

        group.add_option("--logdir",
                         dest="logdir",
                         type="string",
                         help="Set the directory where log files will \
                               be stored (default: %default)",
                         default="/var/log/jarvis-server/")

        group.add_option("--basedir",
                         dest="basedir",
                         type="string",
                         help="Set the directory where sqlite database will \
                               be stored (default: %default)",
                         default="/var/lib/jarvis-server/")

        group.add_option("--log-backup",
                         dest="logbackup",
                         type = "int",
                         help = "Keep DAYS logfile (default: %default)",
                         default = 180,
                         metavar = "DAYS")

        group.add_option("--listen-addr",
                         dest="listen_addr",
                         type="string",
                         help="Set address to listen (default: %default)",
                         metavar="ADDR",
                         default="127.0.0.1")

        group.add_option("--listen-port",
                         dest="listen_port",
                         type="int",
                         help="Set port to listen (default: %default)",
                         metavar="PORT",
                         default=9090)

        group.add_option("--server",
                         dest="wsgi_server",
                         type="string",
                         help="Name of the WSGI server to use \
                               (default: %default)",
                         metavar="SERVER",
                         default="flask")

        group.add_option("-D",
                         "--daemonize",
                         action="store_true",
                         dest="daemonize",
                         help="start server in background")

        group.add_option('-p',
                         '--pidfile',
                         action='store',
                         help='Pid file location (Required)',
                         default=None)

        self.add_option_group(group)

    def check_options_server(self, daemon, options, actions):
        try:
            func = getattr(daemon, options.wsgi_server)
        except AttributeError:
            self.error("%s is not a supported wsgi server"%options.wsgi_server)

        if options.daemonize and not options.pidfile:
            self.error("A pidfile must be supplied in daemon mode")

    def parse_args(self, args=None, values=None):
        global options
        # We must call the parent class ...
        (options, args) = optparse.OptionParser.parse_args(self, args, values)
        self.config = ConfigParser.RawConfigParser()
        self.config.read(options.config_file)
        # Replace default value with data found in the file
        options._update(self.__update_defaults(options), "loose")
        return (options, args)

    def __get_config_section(self, name):
        """Get a section of a configuration"""
        if self.config.has_section(name):
            return self.config.items(name)
        return []

    def __update_defaults(self, defaults={}):
        config = {}
        for section in ('jarvis-server', self.module_name):
            config.update(dict(self.__get_config_section(section)))

        if 'basedir' not in config and self.get_option('--basedir'):
            config['basedir'] = defaults.basedir

        if 'logdir' not in config and self.get_option('--logdir'):
            config['logdir'] = defaults.logdir

        return config
