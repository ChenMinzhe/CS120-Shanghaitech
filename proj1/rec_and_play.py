"""
Note: All recording outputs are <class 'bytes'> objects.
"""
import pyaudio
import wave
import time

SAMPLE_RATE = 48000
CHUNK = 1024

def rec_and_play_file(filename: str, time_length, output=False,deviceIn=1, deviceOut=5) -> bytes:
    """
    Play a file and record at the same time. Return the recorded bytestream
    """
    p = pyaudio.PyAudio()
    wf = wave.open(filename, 'rb')
    stream_out = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        output_device_index=deviceOut,
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    stream_in = p.open(format=pyaudio.paInt16,
                       input_device_index=deviceIn,
                       channels=1,
                       rate=SAMPLE_RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

    init_time = time.time()

    data_wf = wf.readframes(CHUNK)
    frames = []

    print("* recording")

    while time.time() - init_time < time_length:
        stream_out.write(data_wf)
        data_wf = wf.readframes(CHUNK)
        data_rec = stream_in.read(CHUNK)
        frames.append(data_rec)
    wf.close()
    stream_out.stop_stream()
    stream_out.close()
    stream_in.stop_stream()
    stream_in.close()
    print("* done recording")

    p.terminate()
    return b''.join(frames)

def play_bytestream_without_pause(bytestream: bytes, deviceOut = 5) -> None:
    """
    Play the given bytestream.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    output_device_index=deviceOut,
                    channels=1,
                    rate=SAMPLE_RATE,
                    frames_per_buffer=10,
                    output=True)
    
    stream.write(bytestream)

    #time.sleep(1)


def play_bytestream(bytestream: bytes, deviceOut = 5) -> None:
    """
    Play the given bytestream.
    """
    frames_out = []
    i = 0

    while i*CHUNK < len(bytestream):
        frames_out.append(bytestream[i*CHUNK:(i+2)*CHUNK])
        i += 2
    frames_out.reverse()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    output_device_index=deviceOut,
                    channels=1,
                    rate=SAMPLE_RATE,
                    #frames_per_buffer=int(len(bytestream) * 0.5),
                    output=True)
    
    while frames_out:
        stream.write(frames_out.pop())

    time.sleep(1)

def rec_and_play_stream(bytestream: bytes, sampwidth: int, output=False, deviceIn=1, deviceOut=5) -> bytes:
    """
    Play the given bytestream and record simultaneously. Return the recorded bytestream.
    """
    frames_out = []
    i = 0

    while i*CHUNK < len(bytestream):
        frames_out.append(bytestream[i*CHUNK:(i+2)*CHUNK])
        i += 2
    frames_out.reverse()

    p = pyaudio.PyAudio()
    stream_out = p.open(format=pyaudio.paInt16,
                        output_device_index=deviceOut,
                        channels=1,
                        rate=SAMPLE_RATE,
                        output=True)

    stream_in = p.open(format=pyaudio.paInt16,
                       input_device_index=deviceIn,
                       channels=1,
                       rate=SAMPLE_RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

    frame_in = []

    #print("* recording")
    while frames_out:
        stream_out.write(frames_out.pop())
        data_in = stream_in.read(CHUNK)
        frame_in.append(data_in)

    stream_out.stop_stream()
    stream_out.close()
    stream_in.stop_stream()
    stream_in.close()
    #print("* done recording")

    p.terminate()
    return b''.join(frame_in)

def record(time_length, deviceIn = 1):
    p=pyaudio.PyAudio()
    stream_in = p.open(format=pyaudio.paInt16,
                       input_device_index=deviceIn,
                       channels=1,
                       rate=SAMPLE_RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
    frames=[]
    init_time=time.time()
    #print("* recording")
    while time.time()-init_time < time_length:
        frames.append(stream_in.read(CHUNK))
    #print("* done recording")
    return b''.join(frames)


def record_without_pause(time_length, deviceIn = 1):
    p=pyaudio.PyAudio()
    stream_in = p.open(format=pyaudio.paInt16,
                       input_device_index=deviceIn,
                       channels=1,
                       rate=SAMPLE_RATE,
                       input=True,
                       frames_per_buffer=int(SAMPLE_RATE*time_length))
    #print("* recording")
    frame=stream_in.read(int(SAMPLE_RATE*time_length))
    #print("* done recording")
    return frame

def write_bytestream_to_wave(bytestream, filename):
    with wave.open(filename, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(bytestream)

if __name__ == '__main__':
    #with wave.open("test.wav", "rb") as w:
    #    wf = w.readframes(SAMPLE_RATE * 10)
    #recorded = rec_and_play_stream(wf, True)
    #play_bytestream(recorded)
    pass