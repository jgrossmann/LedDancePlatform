"""
Written by John Grossmann
"""

import os
import socket
import time
import select
import threading
import subprocess

class ServerSocketConnection(object):
    #Creates a simple unix socket listener for same computer communication
    def __init__(self, path):
        self.path = path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    def connectToSocket(self):
        if(os.path.exists(self.path)):
            os.remove(self.path)
        self.sock.bind(self.path)
        self.sock.listen(1)
        c,addr = self.sock.accept()
        self.client = c
        

    def listen(self, time):
        read, write, error = select.select([self.client],[],[],time)
        if(len(read) > 0):
            data = read[0].recv(2048)
            return data
        return False

    def send(self, data, time):
        read, write, error = select.select([],[self.client],[],time)
        if(len(write) > 0):
            write[0].send(data)

    def disconnectSocket(self):
        self.sock.close()
        os.remove(self.path)

if __name__ == "__main__":
    sock = ServerSocketConnection("/tmp/Led_Dance_Platform_Socket")
    thread = threading.Thread(target=sock.connectToSocket, args=())
    thread.start()
    print "past thread"
    sub = subprocess.Popen(["node","/home/john/LedDancePlatform/LedPlatformServer.js"])
    thread.join()
    
    #s = sock.connectToSocket()
    print sock.listen(10)
    sock.disconnectSocket()
    print "done"
    sub.kill()
        
        
