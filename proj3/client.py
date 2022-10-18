import sys, socket, os, re, time


class FTPClient():
    currentPath = "/"

    def __init__(self):
        self.controlSock = None
        self.bufSize = 1024
        self.connected = False
        self.loggedIn = False
        self.dataMode = 'PORT'
        self.dataAddr = None
    def parseReply(self, bprint = True):
        #time.sleep(0.1)
        if self.controlSock == None:
            return
        try:
            reply = self.controlSock.recv(self.bufSize).decode('ascii')
        except (socket.timeout):
            return
        else:
            if 0 < len(reply):
                output = '<< ' + reply.strip().replace('\n', '\n<< ')
                time.sleep(1.1)
                if(bprint):
                    print(output)
                return (int(reply[0]), reply)
            else: # Server disconnected
                self.connected = False
                self.loggedIn = False
                self.controlSock.close()
                self.controlSock = None
    def connect(self, host, port, bprint = True):
        
        if self.controlSock != None: # Close existing socket first
            self.connected = False
            self.loggedIn = False
            self.controlSock.close()
        self.controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.controlSock.connect((host, port))
        if self.parseReply(bprint)[0] <= 3:
            self.connected = True
            self.controlSock.settimeout(1.0) # Timeout 1 second
    def login(self, user, password, bprint = True):
        if not self.connected:
            return
        self.loggedIn = False
        self.controlSock.send(('USER %s\r\n' % user).encode('ascii'))
        if self.parseReply(bprint)[0] <= 3:
            self.controlSock.send(('PASS %s\r\n' %password).encode('ascii'))
            if self.parseReply(bprint)[0] <= 3:
                self.loggedIn = True
    def quit(self, bprint = True):
        if not self.connected:
            return
        self.controlSock.send(b'QUIT\r\n')
        self.parseReply(bprint)
        self.connected = False
        self.loggedIn = False
        self.controlSock.close()
        self.controlSock = None
    def pwd(self):
        if not self.connected or not self.loggedIn:
            return
        self.controlSock.send(b'PWD\r\n')
        self.parseReply()
    def cwd(self, path, bprint = True):
        if not self.connected or not self.loggedIn:
            return
        self.controlSock.send(('CWD %s\r\n' % path).encode('ascii'))
        self.parseReply(bprint)
        time.sleep(0.2)
        self.controlSock.send(b'PWD\r\n')
        self.currentPath = self.parseReply(False)[1].split()[1][1:-1]
        #print(self.currentPath)
    def help(self):
        if not self.connected or not self.loggedIn:
            return
        self.controlSock.send(b'HELP\r\n')
        self.parseReply()
    def type(self, t):
        if not self.connected or not self.loggedIn:
            return
        self.controlSock.send(('TYPE %s\r\n' % t).encode('ascii'))
        self.parseReply()
    def pasv(self, bprint = True):
        self.controlSock.send(b'PASV\r\n')
        reply = self.parseReply(bprint)
        if reply[0] <= 3:
            m = re.search(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', reply[1])
            self.dataAddr = (m.group(1) + '.' + m.group(2) + '.' + m.group(3) + '.' + m.group(4), int(m.group(5)) * 256 + int(m.group(6)))
            self.dataMode = 'PASV'
    def nlst(self):
        if not self.connected or not self.loggedIn:
            return
        if self.dataMode != 'PASV': # Currently only PASV is supported
            print("Not passive mode")
            return
        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        dataSock.connect(self.dataAddr)
        self.controlSock.send(b'NLST\r\n')
        time.sleep(0.5) # Wait for connection to set up
        dataSock.setblocking(False) # Set to non-blocking to detect connection close
        while True:
            try:
                data = dataSock.recv(self.bufSize)
                if len(data) == 0: # Connection close
                    break
                print(data.decode('ascii').strip())
            except (socket.error): # Connection closed
                break
        dataSock.close()
        self.parseReply()
    def retr(self, filename):
        if not self.connected or not self.loggedIn:
            return
        if self.dataMode != 'PASV': # Currently only PASV is supported
            return
        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        dataSock.connect(self.dataAddr)
        self.controlSock.send(('RETR %s\r\n' % filename).encode('ascii'))
        fileOut = open(filename, 'wb')
        time.sleep(0.5) # Wait for connection to set up
        dataSock.setblocking(False) # Set to non-blocking to detect connection close
        while True:
            try:
                data = dataSock.recv(self.bufSize)
                if len(data) == 0: # Connection close
                    break
                fileOut.write(data)
            except (socket.error): # Connection closed
                break
        fileOut.close()
        dataSock.close()
        self.parseReply()
    def stor(self, filename):
        if not self.connected or not self.loggedIn:
            return
        if self.dataMode != 'PASV': # Currently only PASV is supported
            return
        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        dataSock.connect(self.dataAddr)
        self.controlSock.send(('STOR %s\r\n' % filename).encode('ascii'))
        dataSock.send(open(filename, 'rb').read())
        dataSock.close()
        self.parseReply()
