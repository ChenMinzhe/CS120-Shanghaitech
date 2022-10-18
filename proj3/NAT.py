import socket
import _thread
import time
import random
import ping

#import SEND_AND_PRAY as sap
import psk_modulator as pm
import rec_and_play  as rap

with open("INPUT.txt") as f:
    sendtxt = f.read().split("\n")
for i in range(len((sendtxt))):
    sendtxt[i] += (40-len(sendtxt[i]))*" "
ipAddress = [item[4][0] for item in socket.getaddrinfo(socket.gethostname(),None) if ':' not in item[4][0]][0]

def tbin(intnum):
    r = ''
    if intnum:
        r = tbin(intnum//2)
        return r + str(intnum%2)
    else:
        return r

def char_to_bytestring(char):
    return ((8-len(tbin(ord(char))))*"0" + tbin(ord(char)))

def string_to_bytestring(string):
    ostr = ""
    for char in string:
        ostr += ((8-len(tbin(ord(char))))*"0" + tbin(ord(char)))
    return ostr

def IP_to_bytestring(IP, index):
    templist = IP.split(".")
    ostr = ""
    for char in templist:
        ostr += ((8-len(tbin(int(char))))*"0" + tbin(int(char)))
    ostr += ((8-len(tbin(index)))*"0" + tbin(index))
    return ostr    
        
def file_to_bytestring(filename):
    bytestring = ""
    with open(filename, encoding="utf-8") as d:
        content = d.read().split("\n")
    for i in range(len(content)):
        for j in range(len(content[i])):
            bytestring += char_to_bytestring(content[i][j])
    return bytestring

def bytestring_to_file(string, length = 1200, lines = 30):
    f=open('Audioreceive.txt', "w")
    for i in range(lines):
        sentance = string[320*i : 320*i + 320]
        writesentance = ""
        for byte in range(40):
            bytestring = sentance[byte*8 : (byte*8+8)]
            try:
                bytenumber = 128*int(bytestring[0]) + 64*int(bytestring[1]) + 32*int(bytestring[2]) + 16*int(bytestring[3]) + 8*int(bytestring[4]) + 4*int(bytestring[5]) + 2*int(bytestring[6]) + 1*int(bytestring[7])
            except:
                bytenumber = 35
            writesentance += chr(bytenumber)
        try:
            f.write(writesentance.strip() + "\n")
        except:
            f.write("#" + "\n")
    f.close()
    
def bytestring_to_string(bytestrings):
    writesentance = ""
    for byte in range(int(len(bytestrings)/8)):
        bytestring = bytestrings[byte*8 : (byte*8+8)]
        try:
            bytenumber = 128*int(bytestring[0]) + 64*int(bytestring[1]) + 32*int(bytestring[2]) + 16*int(bytestring[3]) + 8*int(bytestring[4]) + 4*int(bytestring[5]) + 2*int(bytestring[6]) + 1*int(bytestring[7])
        except:
            bytenumber = 35
        writesentance += chr(bytenumber)
    return writesentance

def bytes_to_bytestring(byte):
    output = ""
    for i in byte:
        output += ((8-len(tbin(i)))*"0" + tbin(i))
    return output

def IPextract(string):
    #print(string)
    bytenumber = [0,0,0,0,0]
    for byte in range(5):
        bytestring = string[byte*8 : (byte*8+8)]
        try:
            bytenumber[byte] = 128*int(bytestring[0]) + 64*int(bytestring[1]) + 32*int(bytestring[2]) + 16*int(bytestring[3]) + 8*int(bytestring[4]) + 4*int(bytestring[5]) + 2*int(bytestring[6]) + 1*int(bytestring[7])
        except:
            bytenumber[byte] = 35
    return str(bytenumber[0]) + "." +str(bytenumber[1]) + "." + str(bytenumber[2]) + "." + str(bytenumber[3]) + " " + str(bytenumber[4]) + " "

def format_file(file, lines = 30, char_per_line = 40):
    with open(file) as f:
        line_list = f.read().split("\n")
    ostr = ""
    for i in range(lines):
        ostr += line_list[i]+(char_per_line-len(line_list[i]))*" "
    return ostr
        
def UDPsender(filename):
    with open(filename) as f:
        sendtxt = f.read().split("\n")
    for i in range(len((sendtxt))):
        sendtxt[i] += (40-len(sendtxt[i]))*" "    
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for txt in sendtxt:
        s.sendto((ipAddress + " 100 " + txt).encode(),(ipAddress,1000))
        #time.sleep(1)

def UDPreceiver(lines = 30):
    f=open('UDPreceive.txt', "wb")
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(("10.20.201.41",1000))
    #print(ipAddress)
    for i in range(lines):
        data=s.recv(1024).decode().strip()+'\r\n'
        print(data.strip())
        f.write(bytes(data.encode()))
    f.close()
    
def UDPreceive_one_message():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((ipAddress,1000))
    data=s.recv(1024).decode().strip()+'\r\n'
    print(data.strip())
    return data
    
def E_listen_A_send(Eline = 30):
    UDPreceiver(Eline)
    #print(len(file_to_bytestring("UDPreceive.txt")))
    output = pm.encode(file_to_bytestring("UDPreceive.txt"), 0)
    #rap.play_bytestream_without_pause(output)
    rap.write_bytestream_to_wave(output, "out.wav")
    

def A_listen_E_send(Tlisten = 25):
    pass

def NATping(ipaddress = "192.168.1.1"): 
    packet_id = int((id(1) * random.random()) % 65535)
    packet = ping.create_packet(packet_id)
    ICMP_packet_string = bytes_to_bytestring(packet)
    for i in range(10):
        #start thread listen
        
        
        #send one packet by audio
        #at the same time listen by audio
        #print what received
        continue
    return


if __name__ == '__main__':
    NATping()
    while(1):
        pass