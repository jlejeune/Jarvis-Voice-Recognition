# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import logging
from flask import jsonify, Blueprint
from jarvis.flask.models.epg import Epg
from jarvis.actions.httpGET import EPG_URLS

epg = Blueprint('epg', __name__)

logger = logging.getLogger('jarvis-server.epg')


### GET methods ###
@epg.route('/epg/<stream>', methods=['GET'])
@epg.route('/epg', methods=['GET'])
def get_epg(stream=None):
    """
    Get epg from given stream or get full epg if no one stream is given
    @param stream    : stream
    """
    if stream != None and stream.encode('utf8', "ignore") not in EPG_URLS:
        return 'Your given stream %s is not defined in  [%s]'\
                    % (stream.encode('utf8', "ignore"),
                       ', '.join(EPG_URLS.keys())), 500

    # Init epg instance and return variable
    selector = Epg()
    epg = dict()

    if stream == None:
        try:
            elmts = selector.get_full_epg()
        except Exception, err:
            logger.exception(err)
            return str(err), 500

        # Init output dict
        for stream in EPG_URLS:
            epg[stream] = list()
    else:
        # Encode in utf8 given param (it's in unicode)
        stream = stream.encode('utf8', "ignore")
        try:
            elmts = selector.get_epg(stream)
        except Exception, err:
            logger.exception(err)
            return str(err), 500

        # Init output dict
        epg[stream] = list()

    # Save values in output variable
    for prog in elmts:
        epg[prog.stream.encode('utf8', "ignore")].append(prog.to_json())

    return jsonify(epg)

@epg.route('/epg/<stream>/full', methods=['GET'])
@epg.route('/epg/full', methods=['GET'])
def get_full_epg(stream=None):
    """
    Get full epg from given stream or get full epg if no one stream is given
    @param stream    : stream
    """
    if stream != None and stream.encode('utf8', "ignore") not in EPG_URLS:
        return 'Your given stream %s is not defined in  [%s]' % (stream,
               ', '.join(EPG_URLS.keys())), 500

    # Init epg instance and return variable
    selector = Epg()
    epg = dict()

    if stream == None:
        try:
            elmts = selector.get_full_epg(full=True)
        except Exception, err:
            logger.exception(err)
            return str(err), 500

        # Init output dict
        for stream in EPG_URLS:
            epg[stream] = list()
    else:
        # Encode in utf8 given param (it's in unicode)
        stream = stream.encode('utf8', "ignore")
        try:
            elmts = selector.get_epg(stream, full=True)
        except Exception, err:
            logger.exception(err)
            return str(err), 500

        # Init output dict
        epg[stream] = list()

    # Save values in output variable
    for prog in elmts:
        epg[prog.stream.encode('utf8', "ignore")].append(prog.to_json())

    return jsonify(epg)

@epg.route('/epg/streams', methods=['GET'])
def get_streams():
    """
    Get a list of all streams
    """
    return jsonify(streams=EPG_URLS.keys())

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
