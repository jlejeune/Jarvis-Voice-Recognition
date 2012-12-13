#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import gst
import gobject
from urllib2 import Request, urlopen
import textwrap

MAX_WRAP = 100

'''
This class permits to generate speech via Google Translate Text-o-Speech API.

Need packages :
    - python-gst
    - python-gobject
'''

class synthesizer():
    def __init__(self):
        self.player = None
        # Instantiate the mainloop even if not used
        self.mainloop = gobject.MainLoop()

    def on_finish(self, bus, message):
        '''
        Callback triggered at the end of the stream
        '''
        self.player.set_state(gst.STATE_NULL)
        self.mainloop.quit()

    def say(self, text, lang="fr", volume=3.0):
        for splitted_lines in textwrap.wrap(text, MAX_WRAP):
            music_stream_uri = 'http://translate.google.com/translate_tts?' + \
                    'q=' + splitted_lines + '&tl=' + lang + "&ie=UTF-8"
            # Create the player
            self.player = gst.element_factory_make("playbin", "player")
            # Provide the source which is a stream
            self.setUri(music_stream_uri)
            # Val from 0.0 to 10 (float)
            self.setVolume(volume)
            # Play
            self.player.set_state(gst.STATE_PLAYING)

            # Get the bus (to send catch connect signals..)
            bus = self.player.get_bus()
            bus.add_signal_watch_full(1)
            # Connect end of stream to the callback
            bus.connect("message::eos", self.on_finish)
            # Wait an event
            self.mainloop.run()

    def sayNB(self, text, lang="fr", volume=3.0):
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
        self.setUri(music_stream_uri)
        # Val from 0.0 to 10 (float)
        self.setVolume(volume)
        # Play
        self.player.set_state(gst.STATE_PLAYING)

    def download(self, text, lang="en", filename="translate_tts"):
        req = Request(url='http://translate.google.com/translate_tts')
        # Needed otherwise return 403 Forbidden
        req.add_header('User-Agent', 'My agent !')
        req.add_data("tl=" + lang + "&q=" + text + "&ie=UTF-8")
        fin = urlopen(req)
        mp3 = fin.read()
        fout = file(filename + ".mp3", "wb")
        fout.write(mp3)
        fout.close()

    def setVolume(self, val):
        # Val from 0.0 to 10 (float)
        self.player.set_property('volume', val)

    def setUri(self, val):
        self.player.set_property('uri', val)

if __name__ == "__main__":
    input_string = sys.argv

    if len(input_string) < 3:
        print("Usage: python %s language_code Your text separated with spaces."
                % input_string[0])
        sys.exit(1)

    # Remove the program name from the argv list
    input_string.pop(0)
    # Take the language which should be now the first args
    lang = input_string[0]
    input_string.pop(0)
    # Convert to url all the rest (with + replacing spaces)
    tts_string = '+'.join(input_string)

    synthesizer().say(tts_string, lang)
    #synthesizer().download(tts_string, lang)

    sys.exit(0)
