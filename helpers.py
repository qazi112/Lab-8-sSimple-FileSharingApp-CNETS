
import os
from pathlib import Path
PATH = "D:\Semester 6\CNets Lab\lab8\FILES"
# e.g request = "0x0000"[2:] and output b'\x00\x00'
def convertHex_request_bytes(request):
    return bytes.fromhex(request)

def convert_to_hex (request):
    return request.hex()


def getNumberOfFiles(PATH):
    return len(os.listdir(PATH))

def getFilesList(PATH):
    return os.listdir(PATH)

def is_file_exists(filename):
    for file in os.listdir(PATH):
        if filename.lower() == file.lower():
            return True
        else:
            False 

def get_file_size(filename):
    filename = Path(PATH,filename)
    return os.path.getsize(filename)