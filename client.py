import socket
import os
import time
import psutil
#Fill in the below with your server IP and Port
ip = "your.ip.here"
port = 5000 #must be an integer (no quotation marks)


if os.name == "nt":
    try:
        hostname = os.popen("C:\\Windows\\System32\\HOSTNAME.EXE").read().strip()
    except Exception as e:
        hostname = socket.gethostbyname()
if os.name == "posix":
    try:
        hostname = os.popen("/usr/bin/hostname").read().strip()
    except Exception as e:
        hostname = socket.gethostbyname()
if os.name != "nt" and os.name != "posix":#fall back (idek why i kept os specific methods for hostname but wtv ig)
    hostname = socket.gethostbyname()


def checkcpu():
    return str(int(psutil.cpu_percent())) + "%"

def checkram():
    inUseMemory = psutil.virtual_memory().used / (1024**3)
    totalMemory = psutil.virtual_memory().total / (1024**3)
    return str(round(inUseMemory, 1)) + "/" + str(round(totalMemory, 1)) + "GB"


def start_client():
    global ip
    global port
    host = ip
    port = port
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        
        while True:
            message = (hostname + " " + checkcpu() + " " + checkram())
            client_socket.send(message.encode())

            
            response = client_socket.recv(1024).decode()
            time.sleep(1)

    except Exception as e: #auto reconnect
        print(e)
        client_socket.close()

while True:
    start_client()
    time.sleep(5)
