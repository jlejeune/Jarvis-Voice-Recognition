# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import os
import logging
from flask import Blueprint
from jarvis.synthesizer import synthesizer

tts = Blueprint('tts', __name__)

logger = logging.getLogger('jarvis-server.tts')


### GET methods ###
@tts.route('/tts/<text>', methods=['GET'])
def speak(text):
    """
    Speech given text
    @param text : string
    """
    synthesizer().say(text, 'fr')
    return 'OK'

@tts.route('/tts/play/<path:filename>', methods=['GET'])
def play_sound(filename):
    """
    Play given mp3 file
    @param filename : mp3 file you want to play (without first /)
    """
    if os.path.exists('/' + filename):
        synthesizer().play('/' + filename)
        return 'OK'
    else:
        return 'Given filename /%s does not exist' % filename, 400
