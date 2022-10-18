import psk_modulator
import rec_and_play
import math
'''
with open("output.txt", "w") as f:
    print(psk_modulator.decode(), file=f)


'''
d = psk_modulator.decode()
t = ''
for i in range(0,50000):
    t+=d[i]

o=open('OUTPUT.bin', "wb")
o.write(bytes(int(t[i*8:(1+i)*8],2) for i in range(0,6250)))
o.close()
