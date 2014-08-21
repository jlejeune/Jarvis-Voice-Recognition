#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request
from functools import wraps

from jarvis.synthesizer import synthesizer


def tts_callback(func):
    """Wraps Text-To-Speech output for requests"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback == 'tts':
            data = func(*args, **kwargs).data
            if data == '' or not isinstance(data, str):
                data = "Nothing to say!" 
            synthesizer().say(data, 'fr')
            return ('', 204)
        else:
            return func(*args, **kwargs)
    return decorated_function
