import socket

ICMP_HEADER = b'x08\x00\x00\x00\x00\x00\x00'
ipadd = socket.gethostbyname('220.181.38.148')
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
#s = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
s.sendto(ICMP_HEADER, ('192.168.31.51', 2000))
reply = s.recv(1024)
print(reply)