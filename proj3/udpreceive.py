import socket
import _thread
import time

ipAddress = [item[4][0] for item in socket.getaddrinfo(socket.gethostname(),None) if ':' not in item[4][0]][0]

def UDPreceiver():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((ipAddress,100))
    while(1):
        data=s.recv(1024) 
        print(ipAddress,100,data.decode())
        time.sleep(1)

if __name__ == '__main__':
    UDPreceiver()