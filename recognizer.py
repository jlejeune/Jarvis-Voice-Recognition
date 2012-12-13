#!/usr/bin/python
# -*- coding: utf-8 -*-

from synthesizer import synthesizer
from actions.httpGET import httpGET

'''
This class permits to analyse speech to execute some actions.

'''


class recognizer():
    def __init__(self):
        pass

if __name__ == "__main__":
    # Ask menu
    website = "http://www.lafinemousse.fr/carte"
    get = httpGET(website)
    tts_string = ',+'.join(get.return_menu()).replace(' ', '+')
    synthesizer().say(tts_string)
