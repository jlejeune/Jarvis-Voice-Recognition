#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import os
import sys

RATE = 16000

if __name__ == "__main__":
    input_string = sys.argv

    if len(input_string) < 2:
        print("Usage: python %s flac_filepath." % input_string[0])
        sys.exit(1)

    filepath = input_string[1]

    if not os.path.exists(filepath):
        print filepath, 'doesn\'t exist'
        sys.exit(1)

    f = open(filepath, 'rb')
    url = 'https://www.google.com/speech-api/v1/recognize?xjerr=1&client=speech2text&lang=fr&maxresults=1'
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'audio/x-flac; rate=' + str(RATE))
    req.add_header('Accept-Charset', 'utf-8')
    req.add_data(f.read())
    f.close()
    data = urllib2.urlopen(req)

    a = json.loads(data.read())
    try:
        print 'CONFIDENCE :', float(a['hypotheses'][0]['confidence'])*100, '%'
        print 'UTTERANCE :', a['hypotheses'][0]['utterance']
    except Exception, err:
        print err, a
