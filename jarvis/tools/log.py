# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import os
import sys
import logging
import logging.config
from flask import request


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        if not request:
            log_record.url = ""
            log_record.method = ""
            log_record.ip = ""
            return True
        log_record.url = request.path
        log_record.method = request.method
        log_record.ip = request.environ.get("REMOTE_ADDR")
        return True


def configure_logging(app):
    del app.logger.handlers[:]
    if app.config.get("API_LOGGING"):
        logging.config.dictConfig(app.config['API_LOGGING'])
    else:
        if app.config.get("verbose"):
            loglevel = logging.DEBUG
        else:
            loglevel = logging.INFO
        logging.getLogger().setLevel(loglevel)

        # Define logging format
        format_string = "%(asctime)s %(name)s %(levelname)s %(message)s"
        datefmt = '[%Y-%m-%d %H:%M:%S]'

        if app.config.get("logdir") and app.config["logdir"] != "":
            logger = logging.getLogger('jarvis-server')
            info_log = os.path.join(app.config["logdir"], "jarvis-server_info.log")
            handler = logging.handlers.TimedRotatingFileHandler(info_log,
                                                                'midnight',
                                                                app.config["logbackup"])
            handler.setLevel(loglevel)
            handler.setFormatter(logging.Formatter(fmt=format_string,
                                                   datefmt=datefmt))
            logger.addHandler(handler)

        if sys.stdin.isatty():
            logger = logging.getLogger()
            handler = logging.StreamHandler()
            handler.setLevel(loglevel)
            handler.setFormatter(logging.Formatter(fmt=format_string,
                                                   datefmt=datefmt))
            logger.addHandler(handler)
