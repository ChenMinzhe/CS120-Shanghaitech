import psk_modulator
import rec_and_play
import math
'''
with open("case.txt", encoding="utf-8") as f: #"case.txt", encoding="utf-8"
    content = f.read().strip()
output = psk_modulator.encode(content, 0)


'''
content = ''
f = open('INPUT.bin','rb')
fbytes = f.read()

for i in range(6250):
    content += (10-len(bin(fbytes[i])))*'0' + bin(fbytes[i])[2:len(bin(fbytes[i]))]
output = psk_modulator.encode(content, 0)

#rec_and_play.play_bytestream_without_pause(output)
rec_and_play.write_bytestream_to_wave(output, "out.wav")
