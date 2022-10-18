import socket
import _thread
import time
import random

ipAddress = [item[4][0] for item in socket.getaddrinfo(socket.gethostname(),None) if ':' not in item[4][0]][0]


def UDPsender():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    while(1):
        randtxt = "".join([random.choice("01") for _ in range(20)])
        print(randtxt)
        s.sendto(randtxt.encode(),("10.20.203.209",100))
        time.sleep(1)

if __name__ == '__main__':
    UDPsender()
    while(1):
        pass