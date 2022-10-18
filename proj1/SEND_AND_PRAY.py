import psk_modulator
import rec_and_play
import math
import _thread
import numpy
import scipy
import time
import sounddevice_instructions as si
import matplotlib.pyplot as plt
import pyaudio
import os
from io import BytesIO
from rec_and_play import SAMPLE_RATE, CHUNK
from psk_modulator import FREQ, HEADER_LENGTH, bits_per_frame, samples_per_bit, header, carrier_wave

final_string = []
#get IO device index

SENDER   = 'CS120-1 (2- USB Audio Device)'
RECEIVER = 'CS120-2 (USB Audio Device)'
SENDER_IN    = si.get_input_device_id_by_name(SENDER)
RECEIVER_IN  = si.get_input_device_id_by_name(RECEIVER)
SENDER_OUT   = si.get_output_device_id_by_name(SENDER)
RECEIVER_OUT = si.get_output_device_id_by_name(RECEIVER)

#pre-open sound device IO stream

rs = pyaudio.PyAudio()
streamrs = rs.open(format=pyaudio.paInt16,
                output_device_index=RECEIVER_OUT,
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=1,
                output=True)

ss = pyaudio.PyAudio()
streamss = ss.open(format=pyaudio.paInt16,
                output_device_index=SENDER_OUT,
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=1,
                output=True)
#streamss.stop_stream()

#truncate the output file

f=open('output.txt', "r+")
f.truncate()
link = [0]
#generate ACK frame(make some sound)

RxFrame = psk_modulator.encode(header, 0)[0:3000]

def getFrameContentLength():
    return bits_per_frame * samples_per_bit


#with open("case.txt", encoding="utf-8") as f: #"case.txt", encoding="utf-8"
#    content = f.read().strip()
    
content = ''
f = open('INPUT.bin','rb')
fbytes = f.read()

for i in range(6250):
    content += (10-len(bin(fbytes[i])))*'0' + bin(fbytes[i])[2:len(bin(fbytes[i]))]
print(len(content))

output1 = []
current_frame = []
for i in range(0,10):
    current_frame.append(content[5000*i : 5000*i+5000])
    output1.append(psk_modulator.encode(current_frame[i], 0))

#print(content)
'''
def TxPending():
    recorded_data = [0]
    p=pyaudio.PyAudio()
    stream_in = p.open(format=pyaudio.paInt16,
                       input_device_index=SENDER_IN,
                       channels=1,
                       rate=SAMPLE_RATE,
                       input=True,
                       frames_per_buffer=48)
    
    while(abs(max(recorded_data)) < 400):
        recorded_data=numpy.fromstring(stream_in.read(48,exception_on_overflow = False), dtype=numpy.short)
        #print(recorded_data)
        #recorded_data = numpy.fromstring(rec_and_play.record_without_pause(0.001,SENDER_IN), dtype=numpy.short)
        #print(time.time())
        #recorded_data = b'\x27\x10\x27\x10\x27\x10\x27\x10'
    #rec_and_play.write_bytestream_to_wave(recorded_data, "TxPending.wav")
    return 0
'''
def RxDone():
    #T = time.time()
    #rec_and_play.play_bytestream_without_pause(RxFrame,RECEIVER_OUT)
    
    streamrs.write(RxFrame)
    
    #print(time.time()-T)
    return 0

def sender():
    p=pyaudio.PyAudio()
    stream_in = p.open(format=pyaudio.paInt16,
                   input_device_index=SENDER_IN,
                   channels=1,
                   rate=SAMPLE_RATE,
                   input=True,
                   frames_per_buffer=48)    
    #print("sender begin")
    frames_sent = 0
    while(frames_sent < 10):
        data = 0
        recorded_data = [1,1]
        #streamss.write(psk_modulator.encode_zeros(100,0))
        while(data < 1000):
            #streamss.write(psk_modulator.encode_zeros(5,0))
            recorded_data=numpy.fromstring(stream_in.read(stream_in.get_read_available(), exception_on_overflow = False), dtype=numpy.short)
            try:
                data = abs(float(recorded_data[-1])+float(recorded_data[-2]))
            except:
                data = 0
            #print(data)
            
            #recorded_data = b'\x27\x10\x27\x10\x27\x10\x27\x10'
        #rec_and_play.write_bytestream_to_wave(recorded_data, "TxPending.wav")
        
        #time.sleep(0.1)
        #print('sender sending')
        #print(time.time())
        #rec_and_play.play_bytestream_without_pause(output1[frames_sent],SENDER_OUT)
        streamss.start_stream()
        #streamss.write(psk_modulator.encode_zeros(300,0))
        #time.sleep(0.1)
        streamss.write(output1[frames_sent])
        
        streamss.stop_stream()
        frames_sent += 1
        print('sender sent')
    return

def execute_and_write(write_data):
    
    header_ = header[::-1]
    headmatch = scipy.signal.convolve(write_data, header_)
    
    threshold = numpy.max(headmatch)*0.89
    heads = list(numpy.where(headmatch > threshold)[0])
    #print(heads)
    output = []
    for i in range(len(heads)):
        if i>0 and heads[i] - heads[i-1] < getFrameContentLength()/2:
            continue
        head = heads[i]

        frame = carrier_wave * write_data[head + 1: head + 1 + getFrameContentLength()]
        
        for i in range(bits_per_frame):
            sum_ = numpy.sum(frame[i*samples_per_bit: (i+1)*samples_per_bit], dtype=numpy.double)
            output.append("0" if sum_ > 0 else "1")
            
    new_frame = "".join(output)
    
    #new_frame = '1001001'
    
    final_string.append(new_frame)
    #print("receiver written")    

def receiver():
    frames_received = 0   
    while(frames_received < 10):
        #RxDone()
        _thread.start_new_thread(RxDone,())
        #print(time.time())
        #print('receiver recording')
        #print(time.time())
        record_time = 0.95 if frames_received>0 else 0.85
        recorded_data1 = numpy.fromstring(rec_and_play.record_without_pause(record_time,RECEIVER_IN), dtype=numpy.short)
        #print(time.time())
        
        if(max(recorded_data1) <500):
            print("link error")
            link[0] = 1
            break
        #rec_and_play.write_bytestream_to_wave(recorded_data1, "received.wav")
        _thread.start_new_thread(execute_and_write,(recorded_data1,))
        
        frames_received += 1
    return


if __name__ == '__main__':
    TIME = time.time()
    _thread.start_new_thread(sender,())
    time.sleep(0.1)
    _thread.start_new_thread(receiver,())
    o=open('OUTPUT.bin', "wb")
    while(len(final_string) <10):
        if(link[0] == 1): break
        time.sleep(0.1)
    final = ''
    if(link[0] == 0):
        for i in range(0,10):
            final += final_string[i]
        o.write(bytes(int(final[j*8:(1+j)*8],2) for j in range(0,6250)))
        o.close()
        print(time.time()-TIME)
    