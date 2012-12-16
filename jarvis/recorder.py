#!/usr/bin/python
# -*- coding: utf-8 -*-

from array import array
from struct import unpack, pack
import pyaudio
import wave
import os

THRESHOLD = 500 #200 ?
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNEL = 2
RATE = 44100 #16000 ?
#NQUIT = 40 # number of silent frames before terminating the program

'''
This class permits to record wave using microphone.
    - need flac package to make convertion (wav => flac)
'''


class recorder:
    def __init__(self):
        pass

def is_silent(L):
    "Returns `True` if below the 'silent' threshold"
    return max(L) < THRESHOLD

def normalize(L):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in L)

    LRtn = array('h')
    for i in L:
        LRtn.append(int(i*times))
    return LRtn

def trim(L):
    "Trim the blank spots at the start and end"
    def _trim(L):
        snd_started = False
        LRtn = array('h')

        for i in L:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                LRtn.append(i)

            elif snd_started:
                LRtn.append(i)
        return LRtn

    # Trim to the left
    L = _trim(L)

    # Trim to the right
    L.reverse()
    L = _trim(L)
    L.reverse()
    return L

def add_silence(L, seconds):
    "Add silence to the start and end of `L` of length `seconds` (float)"
    LRtn = array('h', [0 for i in xrange(int(seconds*RATE))])
    LRtn.extend(L)
    LRtn.extend([0 for i in xrange(int(seconds*RATE))])
    return LRtn

def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNEL,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    LRtn = array('h')

    while 1:
        data = stream.read(CHUNK_SIZE)
        L = unpack('<' + ('h'*(len(data)/2)), data) # little endian, signed short
        L = array('h', L)
        LRtn.extend(L)

        silent = is_silent(L)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        #if snd_started and num_silent > 30:
        if snd_started and num_silent > 10:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    LRtn = normalize(LRtn)
    LRtn = trim(LRtn)
    LRtn = add_silence(LRtn, 0.5)
    return sample_width, LRtn

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to `path`"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNEL)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def convert_wav_to_flac(path):
    from subprocess import Popen, PIPE
    cmd = "flac -f " + path
    p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if int(p.returncode) != 0:
        print err.rstrip()
    else:
        os.remove(path)

if __name__ == '__main__':
    print("please speak a word into the microphone")
    path = 'demo.wav'
    record_to_file(path)
    print("done - result written to %s" %path)
    convert_wav_to_flac(path)
    print("convert OK")
