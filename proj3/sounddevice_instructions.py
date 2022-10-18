import os
import sys
import time
import wave
import numpy as np
import array
import sounddevice as sd
from scipy.io import wavfile
import soundfile


class MyException(Exception):
    
    def __init__(self, *args):
        self.args = args


def preliminary_instruction():
   
    drivers_tuple = sd.query_hostapis()
    print(drivers_tuple)

    for driver_msg_dict in drivers_tuple:
        
        print(driver_msg_dict['name'], end=", ")  # MME, Windows DirectSound, ASIO, Windows WASAPI, Windows WDM-KS,

    
    devices_list = sd.query_devices() 
    for device_msg_dict in devices_list:
        print(device_msg_dict)



def get_input_device_id_by_name(channel_name):

    devices_list = sd.query_devices()
    for index, device_msg_dict in enumerate(devices_list):
        if channel_name == device_msg_dict["name"] and device_msg_dict["max_input_channels"] > 0:
            return index
    else:
        raise MyException("cannot find device")


def get_output_device_id_by_name(channel_name):
 
    devices_list = sd.query_devices()
    for index, device_msg_dict in enumerate(devices_list):
        if channel_name == device_msg_dict["name"] and device_msg_dict["max_output_channels"] > 0:
            return index
    else:
        raise MyException("cannot find device")


def read_data(audio_file_path, audio_channels):
    if audio_file_path.endswith(".wav"):
        data_array, sample_rate = soundfile.read(audio_file_path)
        return data_array

    elif audio_file_path.endswith(".pcm") or audio_file_path.endswith(".raw"):
        data_array = array.array('h')
        with open(audio_file_path, "rb") as f:
            data_array.frombytes(f.read())

        data_array = data_array[::audio_channels]
        return data_array


def play_audio_file(audio_file_path, channel_id, audio_channels, sample_rate):

    sd.default.device[1] = channel_id

    data_array = read_data(audio_file_path, audio_channels)
    sd.play(data_array, sample_rate)
    sd.wait() 
    
def do_record(channel_id, file_path):
    sd.default.device[0] = channel_id

    sample_rate = 44100 
    length = 10 
    record_data = sd.rec(frames=length*sample_rate, samplerate=sample_rate, channels=1, blocking=True) 
    wavfile.write(file_path, sample_rate, record_data)
    
def play_and_record(input_channel_id, output_channel_id, play_audio_file_path, rec_file_path, play_audio_channels=1,
                    play_audio_fs=44100, rec_file_channels=1):

    sd.default.device[0] = input_channel_id
    sd.default.device[1] = output_channel_id
    data_array = read_data(play_audio_file_path, play_audio_channels)
    rec_data = sd.playrec(data=data_array, samplerate=play_audio_fs, channels=rec_file_channels, blocking=True)
    wavfile.write(rec_file_path, play_audio_fs, rec_data)


if __name__ == "__main__":
    #preliminary_instruction()
    #print(get_output_device_id_by_name('CS120-1 (2- USB Audio Device)'))
    pass

