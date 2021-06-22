from threading import Thread
import socket
import time
from multiThreadedClient import MultiThreadClient


ADDRESS = "127.0.0.1"
PORT = 5050

bufsize = 1024
scheme = "utf-8"

print(f"Server =>  {ADDRESS} : {PORT}")


with socket.socket() as s:
    s.bind((ADDRESS,PORT))
    s.listen(5)
    while True:
        conn,addr = s.accept()
        print(f"Client : {addr}, connected! ")
        client = MultiThreadClient(conn)

        client.start()