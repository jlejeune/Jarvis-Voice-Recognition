# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import logging
from flask import Blueprint
from jarvis.synthesizer import synthesizer

tts = Blueprint('tts', __name__)

logger = logging.getLogger('jarvis-server.tts')


### GET methods ###
@tts.route('/tts/<text>', methods=['GET'])
def get_epg(text):
    """
    Speech given text
    @param text : string
    """
    synthesizer().say(text, 'fr')
    return 'OK'
