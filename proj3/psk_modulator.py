"""
Note: bits_per_frame must be a multiple of 8.
"""
import wave
import numpy
import scipy.signal
import math
import pyaudio
import time
import rec_and_play
from rec_and_play import SAMPLE_RATE, CHUNK
from collections import deque

FREQ = 10000

with open("header.txt") as f:
    head = f.read()
header = head.split()
header = list(map(float, header))

HEADER_LENGTH = 220

bits_per_frame = 90
samples_per_bit = 5

def getFrameContentLength():
    return bits_per_frame * samples_per_bit

carrier_wave = numpy.sin(2*numpy.pi*FREQ*numpy.arange(getFrameContentLength())/SAMPLE_RATE)

def decode(slient_timeout = 5, filename=None):
    """
    Input: Received bytestream.
    Output: Original byte stream.
    """
    if filename is None:
        recorded_data = numpy.fromstring(rec_and_play.record_without_pause(20), dtype=numpy.short)
        rec_and_play.write_bytestream_to_wave(recorded_data, "received.wav")
    else:
        with wave.open(filename, "rb") as f:
            recorded_data = numpy.fromstring(f.readframes(f.getnframes()), dtype=numpy.short)
            
            
    init_time=time.time()
    
    header_ = header[::-1]
    headmatch = scipy.signal.convolve(recorded_data, header_)
    threshold = numpy.max(headmatch)*0.75
    print(threshold)
    heads = list(numpy.where(headmatch > threshold)[0])

    output = []
    for i in range(len(heads)):
        if i>0 and heads[i] - heads[i-1] < getFrameContentLength():
            continue
        head = heads[i]
        frame = carrier_wave * recorded_data[head + 1: head + 1 + getFrameContentLength()]
        for i in range(bits_per_frame):
            sum_ = numpy.sum(frame[i*samples_per_bit: (i+1)*samples_per_bit], dtype=numpy.double)
            output.append("0" if sum_ > 0 else "1")
            
            
    #print(time.time() - init_time)
    return "".join(output)

def decode_buffer():
    return

def decode_frame(bytestream: bytes):
    pass

def encode(string: bytes, sep_per_frame):
    """
    Input: a string consists of 0 and 1
    Output: the encoded signal.

    sep_per_frame: seperate samples between frames.
    """
    frames = []
    for i in range(math.ceil(len(string)/bits_per_frame)):
        frames.append(encode_frame(string[i*bits_per_frame : (i+1)*bits_per_frame]))
    output = bytes(2*sep_per_frame).join(frames)
    #print(output)
    return b''.join([output, bytes(4*sep_per_frame)])


def encode_frame(string: bytes):
    """
    Input: A string consists of 0 and 1
    Output: the modulated signal, including header
    """
    send_frame = numpy.zeros(HEADER_LENGTH + getFrameContentLength(), dtype=numpy.double)
    send_frame[:HEADER_LENGTH] = header
    send_frame[HEADER_LENGTH:] = carrier_wave

    for i in range(len(string)):
        if string[i] != "0":
            send_frame[HEADER_LENGTH + (i)*samples_per_bit: HEADER_LENGTH + (i+1)*samples_per_bit] *= -1
    return (send_frame*10000).astype(numpy.short).tostring()

def encode_zeros(amount,sep_per_frame):
    frames = []
    frames.append(numpy.zeros(amount, dtype=numpy.double).astype(numpy.short).tostring())
    output = bytes(2*sep_per_frame).join(frames)
    #print(output)
    return b''.join([output, bytes(4*sep_per_frame)])    



