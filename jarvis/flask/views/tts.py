# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import os
import logging
from datetime import datetime
from flask import Blueprint
from jarvis.synthesizer import synthesizer
from jarvis.flask import options

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
        synthesizer().playNB('/' + filename)
        return 'OK'
    else:
        return 'Given filename /%s does not exist' % filename, 400

@tts.route('/tts/save/<text>', methods=['GET'])
def save_sound(text):
    """
    save given text in voicemail
    @param text : string text to save in voicemail
    """
    filename = options.voicemaildir + 'msg_' +\
               datetime.now().strftime('%Y%m%d%H%M%S')
    synthesizer().download(text, filename=filename)
    return 'OK'
