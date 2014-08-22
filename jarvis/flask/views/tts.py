# -*- coding: utf-8 -*-
# vim:set ai et sts=4 sw=4:

import os
import logging
import glob
from datetime import datetime
from flask import Blueprint, jsonify

from jarvis.synthesizer import select_synthesizer, LocalSynthesizer
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
    synthesizer = select_synthesizer()
    synthesizer.say(text)
    return 'OK'


@tts.route('/tts/play/<path:filename>', methods=['GET'])
def play_sound(filename):
    """
    Play given mp3 file
    @param filename : mp3 file you want to play (without first /)
    """
    if os.path.exists('/' + filename):
        LocalSynthesizer().playNB('/' + filename)
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
    LocalSynthesizer().download(text.encode('utf8', "ignore"), filename=filename)
    return 'OK'


@tts.route('/tts/messages', methods=['GET'])
def get_msg():
    """
    Return list of messages from voicemaildir
    """
    return jsonify(messages=[glob.glob(options.voicemaildir + 'msg_*.mp3')])
