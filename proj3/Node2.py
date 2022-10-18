import NAT
import time
import _thread
import socket
import psk_modulator as pm
import rec_and_play as rap
import SEND_AND_PRAY as sap
import client
import pyaudio
import numpy

def waitingMessage():
    p=pyaudio.PyAudio()
    stream_in = p.open(format=pyaudio.paInt16,
                   input_device_index=sap.RECEIVER_IN,
                   channels=1,
                   rate=pm.SAMPLE_RATE,
                   input=True,
                   frames_per_buffer=48)
    data = 0
    recorded_data = [1,1]
    while(data < 1000):
        recorded_data=numpy.fromstring(stream_in.read(stream_in.get_read_available(), exception_on_overflow = False), dtype=numpy.short)
        try:
            data = abs(float(recorded_data[-1])+float(recorded_data[-2]))
        except:
            data = 0

'''
inst = input()
if(inst == "1-3"):
    time.sleep(0.1)
    _thread.start_new_thread(sap.receiver,("NAT",))
    print("done")
    
elif(inst == "3-1"):
    NAT.UDPreceiver()
    #output = pm.encode(NAT.string_to_bytestring(NAT.format_file("UDPreceive.txt")), 0)
    #rap.play_bytestream_without_pause(output)
    #rap.write_bytestream_to_wave(output, "out.wav")
    sap.sender("Node2")
elif(inst == "ping"):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    for i in range(10):
        time.sleep(0.1)
        _thread.start_new_thread(sap.receiver,("ping",))    
else:
    print("wrong input")
'''
while(1):
    waitingMessage()
    print("transmitting")
  
    pass

