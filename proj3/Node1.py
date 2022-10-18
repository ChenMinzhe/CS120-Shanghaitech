import NAT
import psk_modulator as pm
import rec_and_play as rap
import SEND_AND_PRAY as sap
import time
import _thread
import ping
import random
import client
'''
inst = input()
if(inst == "1-3"):
    sap.sender("Node1")
    print("done")
elif(inst == "3-1"):
    time.sleep(0.1)
    _thread.start_new_thread(sap.receiver,("NAT",))
    print("done")

else:
    print("wrong input")
        
        
        
while(1):
    pass

'''

def sendtxt():
    sap.streamss.start_stream()
    sap.streamss.write(pm.encode(NAT.IP_to_bytestring("192.168.1.1", 100), 0))
    sap.streamss.stop_stream()

n2 = client.FTPClient()
server = "ftp.sjtu.edu.cn"
n2.connect(server,21)
user = "anonymous"
folder = "/"
while(1):
    inst = input().split()
    if(inst[0] == "USER"):
        user = inst[1]
    elif(inst[0] == "PASS"):
        #try:
        sendtxt()
        n2.login(user, inst[1])
        
        #except:
        #    print("failed to login")
    elif(inst[0] == "PWD"):
        try:
            sendtxt()
            n2.pwd()
        except:
            print("pwd failed")
    elif(inst[0] == "CWD"):
        try:
            sendtxt()
            folder = inst[1]
            n2.cwd(inst[1])
        except:
            print("invalid path")
    elif(inst[0] == "PASV"):
        try:
            sendtxt()
            n2.pasv()
        except:
            print("pasv failed")
    elif(inst[0] == "LIST"):
        try:
            sendtxt()
            n2.quit(False)
            n2.connect(server,21,False)
            n2.login("anonymous","cc",False)
            n2.pasv(False)
            #print(n2.currentPath)
            n2.cwd(n2.currentPath,False)
            n2.nlst()
        except:
            print("nlst failed")
    elif(inst[0] == "QUIT"):
        try:
            n2.quit()
            n2.connect(server,21)
        except:
            print("quit failed")
    else:
        print("unknown command")