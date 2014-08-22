#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import gst
import gobject
from urllib2 import Request, urlopen
import urllib
import textwrap

from karotz import Karotz


MAX_WRAP = 100

'''
This module uses Synthesizer classes (Karotz or Local one) to create audio from
text content.
'''


def select_synthesizer():
    if Karotz().check_health():
        return KarotzSynthesizer()
    else:
        return LocalSynthesizer()


class KarotzSynthesizer(object):
    def say(self, text):
        Karotz().tts.speak(text)


class LocalSynthesizer(object):
    def __init__(self):
        self.player = None
        # Instantiate the mainloop even if not used
        self.mainloop = gobject.MainLoop()

    def say(self, text, lang="fr", volume=1.5):
        for splitted_lines in textwrap.wrap(text, MAX_WRAP):
            music_stream_uri = 'http://translate.google.com/translate_tts?' + \
                'q=' + splitted_lines + '&tl=' + lang + "&ie=UTF-8"
            # Create the player
            self.player = gst.element_factory_make("playbin", "player")
            # Provide the source which is a stream
            self._setUri(music_stream_uri)
            # Val from 0.0 to 10 (float)
            self._setVolume(volume)
            # Play
            self.player.set_state(gst.STATE_PLAYING)

            # Get the bus (to send catch connect signals..)
            bus = self.player.get_bus()
            bus.add_signal_watch_full(1)
            # Connect end of stream to the callback
            bus.connect("message::eos", self._endCallback)
            # Wait an event
            self.mainloop.run()

    def sayNB(self, text, lang="fr", volume=1.5):
        '''
        NB for Non-Blocking
        '''
        if len(text) > MAX_WRAP:
            print 'BE CAREFUL, your text will be cut because of its size : %s'\
                % len(text)
        text = textwrap.wrap(text, MAX_WRAP)[0]
        music_stream_uri = 'http://translate.google.com/translate_tts?tl=' + \
            lang + '&q=' + text + "&ie=UTF-8"
        # Create the player
        self.player = gst.element_factory_make("playbin", "player")
        # Provide the source which is a stream
        self._setUri(music_stream_uri)
        # Val from 0.0 to 10 (float)
        self._setVolume(volume)
        # Play
        self.player.set_state(gst.STATE_PLAYING)

    def play(self, filename, volume=1.5):
        # Init url from given filename
        url = 'file://' + os.path.abspath(filename)
        # Create the player
        self.player = gst.element_factory_make("playbin", "player")
        # Provide the source which is a stream
        self._setUri(url)
        # Val from 0.0 to 10 (float)
        self._setVolume(volume)
        # Play
        self.player.set_state(gst.STATE_PLAYING)

        # Get the bus (to send catch connect signals..)
        bus = self.player.get_bus()
        bus.add_signal_watch_full(1)
        # Connect end of stream to the callback
        bus.connect("message::eos", self._endCallback)
        # Wait an event
        self.mainloop.run()

    def playNB(self, filename, volume=1.5):
        # Init url from given filename
        url = 'file://' + os.path.abspath(filename)
        # Create the player
        self.player = gst.element_factory_make("playbin", "player")
        # Provide the source which is a stream
        self._setUri(url)
        # Val from 0.0 to 10 (float)
        self._setVolume(volume)
        # Play
        self.player.set_state(gst.STATE_PLAYING)

    def download(self, text, lang="fr", filename="translate_tts"):
        # Open file
        fout = file(filename + ".mp3", "wb")
        for splitted_lines in textwrap.wrap(text, MAX_WRAP):
            req = Request(url='http://translate.google.com/translate_tts')
            # Needed otherwise return 403 Forbidden
            req.add_header('User-Agent', 'My agent !')
            req.add_data("tl=" + lang + "&q=" +
                         urllib.quote_plus(splitted_lines) + "&ie=UTF-8")
            fin = urlopen(req)
            mp3 = fin.read()
            fout.write(mp3)
        fout.close()

    def _endCallback(self, bus, message):
        '''
        Callback triggered at the end of the stream
        '''
        self.player.set_state(gst.STATE_NULL)
        self.mainloop.quit()

    def _setVolume(self, val):
        # Val from 0.0 to 10 (float)
        self.player.set_property('volume', val)

    def _setUri(self, val):
        self.player.set_property('uri', val)

if __name__ == "__main__":
    input_string = sys.argv

    if len(input_string) < 3:
        print("Usage:\npython %s say|download your text separated with spaces\
                \nOR\npython %s play filename you want to play"
              % (input_string[0], input_string[0]))
        sys.exit(1)

    # Remove the program name from the argv list
    input_string.pop(0)
    # Take the action which should be now the first args
    action = input_string.pop(0)

    if action == 'say':
        # Convert to url all the rest (with + replacing spaces)
        tts_string = '+'.join(input_string)
        synthesizer = select_synthesizer()
        synthesizer.say(tts_string)
    elif action == 'download':
        # Convert to url all the rest (with + replacing spaces)
        tts_string = '+'.join(input_string)
        LocalSynthesizer().download(tts_string)
    elif action in ('play'):
        # Take last option that has to be filename
        filename = input_string.pop(0)
        if os.path.exists(filename):
            LocalSynthesizer().play(filename)
        else:
            print 'Given filename %s does not exist' % filename
    else:
        print 'Action must be say|download|play'
        sys.exit(1)

    sys.exit(0)
