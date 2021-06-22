from socket import socket
from threading import Thread
from time import sleep

scheme = "utf-8"
bufsize = 1024

class ClientHandler_Thread(Thread):
    def __init__(self,clientSoc):
        Thread.__init__(self)
        self.clientSoc = clientSoc

    def run(self):
        message = self.clientSoc.recv(bufsize).decode(scheme)
        self.clientSoc.send(f"{message}".encode(scheme))
        # close connection
        self.clientSoc.close()