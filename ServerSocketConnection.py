"""
Written by John Grossmann
"""

import os
import socket
import time
import select

class ServerSocketConnection(object):
    #Creates a simple unix socket listener for same computer communication
    def __init__(self, path):
        self.path = path
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
    def connectToSocket(self):
        if(os.path.exists(self.path)):
            os.remove(self.path)
        self.sock.bind(path)

    def listen(self, time):
        read, write, error = select.select([self.sock],[],[],0.05)
        if(len(read) > 0):
            (data,addr) = self.sock.recvfrom(2048)
            return data
        return False

    def disconnectSocket(self):
        self.sock.close()
        os.remove(self.path)
        
