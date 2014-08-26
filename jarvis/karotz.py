#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This class is a wrapper to OpenKarotz API (http://www.openkarotz.org).
"""

import json
import logging
import requests

#FIXME: move it in configuration file
BASE_URL = 'http://192.168.1.60/cgi-bin'

logger = logging.getLogger(__name__)


class Karotz(object):
    def __init__(self):
        self.session = requests.session()

        # Keep resource classes as attributes of karotz.
        # Pass karotz to resource classes so resource object can use the karotz.
        attributes = {'karotz': self}
        self.tts = type('TTS', (_TTS,), attributes)
        self.state = type('State', (_State,), attributes)

    def request(self, path, method='GET', params=None, data=None,
                files=None, headers=None, timeout=None, raw=False):
        """
        Wrapper around requests.request()

        Prepends BASE_URL to path.
        Parses response as JSON and returns it.
        """
        if not params:
            params = {}

        if not headers:
            headers = {}

        headers['Accept'] = 'application/json'

        url = BASE_URL + path
        logger.debug('url: %s', url)

        try:
            response = self.session.request(method,
                                            url,
                                            params=params,
                                            data=data,
                                            files=files,
                                            headers=headers,
                                            timeout=timeout,
                                            allow_redirects=True)
        except requests.exceptions.ConnectionError, err:
            raise Exception(err)

        logger.debug('response: %s', response)
        if raw:
            return response

        logger.debug('content: %s', response.content)
        try:
            response = json.loads(response.content)
        except ValueError:
            raise Exception('Server didn\'t send valid JSON:\n%s\n%s' % (
                response, response.content))

        if 'return' in response:
            if response['return'] != "0":
                raise Exception(response['error_type'])
        else:
            logger.warn('Response status unknown for request: %s', url)

        return response

    def check_health(self):
        try:
            self.state.get_version()
        except Exception:
            return False
        else:
            return True


class _Action(object):

    karotz = None

    def __init__(self, resource_dict):
        """Constructs the object from a dict."""
        self.__dict__.update(resource_dict)


class _TTS(_Action):

    @classmethod
    def speak(cls, text):
        return cls.karotz.request('/tts?text=%s' % text, method='GET')


class _State(_Action):

    @classmethod
    def get_status(cls):
        return cls.karotz.request('/status', method='GET')

    @classmethod
    def get_version(cls):
        return cls.karotz.request('/get_version', method='GET', timeout=1)


if __name__ == "__main__":
    # TTS example
    try:
        Karotz().tts.speak("toto")
    except Exception, err:
        print err

    # check_health example
    print Karotz().check_health()
