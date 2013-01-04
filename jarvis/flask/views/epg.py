# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

from flask import Blueprint
import logging
import json
from jarvis.actions.httpGET import httpGET, EPG_URLS

epg = Blueprint('epg', __name__)

logger = logging.getLogger('jarvis-server.epg')


### GET methods ###
@epg.route('/epg/<stream>', methods=['GET'])
def get_epg(stream=None):
    """
    Get epg from given stream or get full epg if no one stream is given
    @param stream    : stream
    """
    if stream not in EPG_URLS:
        return 'Your given stream %s is not defined in %s' %(stream,
                EPG_URLS.keys()), 500
    try:
        get = httpGET(EPG_URLS[stream])
        epg = get.return_epg()
    except Exception, err:
        logger.exception(err)
        return str(err), 500 

    return json.dumps(epg, ensure_ascii=False)

#@ws.route('/admin/version', methods=['GET'])
#def get_version():
#    """
#    Get version of WS from __version__.py file
#    """
#    try:
#        from jarvis.__version__ import version
#    except ImportError:
#        version = 'unknown'
#    return str(version)
