
from threading import Thread
from helpers import PATH
from helpers import convertHex_request_bytes,convert_to_hex
from helpers import getFilesList,getNumberOfFiles,is_file_exists
from helpers import get_file_size
from helpers import PATH
import socket
import time
import pickle
SEND_BUFFER = 100
SERVER_CODES = ["0x0010","0x0011","0x0012"]
# when sending the code, trim first two characters and pass from convertHex_request_bytes

scheme = "utf-8"
bufsize = 1024

# ========================================

class MultiThreadClient(Thread):
    def __init__(self, clientSocket):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        
    def run(self):
        request= self.clientSocket.recv(bufsize)
        packet = pickle.loads(request)

        code = convert_to_hex(packet[0])

        if(code == "0000"):
            print("List Request")
            self.list_file_service()

        elif code == "0001":

            print("File Requested")
            filename = str(packet[1])

            if is_file_exists(filename):

                print("File Exists")
                self.clientSocket.send("1".encode(scheme))
                self.download_file_request(filename)

            else:
                self.clientSocket.send("0".encode(scheme))
            

    def list_file_service(self):
        packet = []
        code = SERVER_CODES[0][2:]
        print(code)
        code = convertHex_request_bytes(code) 
        print(code)
        packet.append(code)
        packet.append(int(getNumberOfFiles(PATH)))
        files = getFilesList(PATH)
        print(files)
        packet.append(list(files))
        test = pickle.dumps(packet)
        self.clientSocket.send(test)

    def download_file_request(self,filename):
        filesize = get_file_size(filename)
        packet1 = []
        code = convertHex_request_bytes( SERVER_CODES[1][2:] )
        packet1.append(code)
        packet1.append(filename)
        packet1.append(str(filesize))
        packet1 = pickle.dumps(packet1)
        self.clientSocket.send(packet1)

        self.send_file(filename,filesize)

    def send_file(self,filename,filesize):
        filename = PATH+"\\"+filename
        packet = []
        packet.append(convertHex_request_bytes(SERVER_CODES[2][2:]))

        offset = 0
        sent_bytes = 0
        remaining_bytes = filesize
        
        with open(filename, 'rb') as f:
            while True:
                packet = []
                packet.append(convertHex_request_bytes(SERVER_CODES[2][2:]))
                remaining_bytes = filesize - sent_bytes
                offset = filesize - remaining_bytes

                print(remaining_bytes)

                if(remaining_bytes <= 0):
                    f.close()
                    break
                if remaining_bytes >= SEND_BUFFER:
                    bytes_read = f.read(SEND_BUFFER)

                    if  bytes_read ==b"":
                        break

                    sent_bytes = sent_bytes + SEND_BUFFER
                    remaining_bytes = filesize - sent_bytes

                    packet.append(offset)
                    packet.append(bytes_read)
                    print(packet)
                    data = pickle.dumps(packet)
                    self.clientSocket.send(data)
                   
                else:
                    bytes_read = f.read(remaining_bytes)
                    
                    if  bytes_read ==b"":
                        break

                    sent_bytes = sent_bytes + remaining_bytes
                    remaining_bytes = filesize - sent_bytes
                   
                    packet.append(offset)
                    packet.append(bytes_read)
                    print(packet)
                    data = pickle.dumps(packet)
                    self.clientSocket.send(data)
            f.close()
        
    
        
    
     