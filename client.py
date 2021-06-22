from threading import Thread
import socket
import time
import os
from helpers import convert_to_hex,convertHex_request_bytes
import pickle

CLIENT_DIRECTORY = "D:\Semester 6\CNets Lab\lab8\CLIENT_FILES"

ADDRESS = "127.0.0.1"
PORT = 5050
REQUEST = ["0x0000","0x0001"]
scheme = 'utf-8'
bufsize = 1024

# This socket is connected with main server

s = socket.socket()
s.connect((ADDRESS,PORT))
option = input("Press 'L' for List Of Files and 'D' for File Request ?> ").lower()

if option == "l":

    request = (REQUEST[0])[2:]
    request = convertHex_request_bytes(request)
    # request list of files
    packet = [request," "]
    data = pickle.dumps(packet)
    s.send(data)
    data = s.recv(bufsize)
    received = pickle.loads(data)
    print(convert_to_hex( received[0]))

    print(received[1:])

elif option == "d":
    
    request = (REQUEST[1])[2:]
    request = convertHex_request_bytes(request)
    filename = input("Filename ?> ")
    packet = [request,filename]
    data = pickle.dumps(packet)
    s.send(data)
    if s.recv(bufsize).decode(scheme) == "1":

        print("File Exists on sever!")
        received = s.recv(bufsize)
        received = pickle.loads(received)
        print(convert_to_hex(received[0]))
        print(received)
        filesize = int(received[2])
        print(filesize)

        filename = CLIENT_DIRECTORY+"\\"+filename

        print(filename)
        
        my_data = b""
        while True:

            data = s.recv(bufsize)
            if data == b"":
                break
            if not data:
                break
            data = pickle.loads(data)
            my_data = my_data+data[2]
            if(data[1]+100 >= filesize):
                break

        print(my_data)
        with open(filename,'wb') as file:
            file.write(my_data)
      
        file.close()
    else:
        print("File Don't Exists!")

else:
    print("Wrong !!")





   