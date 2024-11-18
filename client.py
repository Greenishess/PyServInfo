import socket
import os
import time
#Fill in the below with your server IP and Port
ip = "your.ip.here"
port = 5000 #must be an integer (no quotation marks)


if os.name == "nt":
    hostname = os.popen("C:\\Windows\\System32\\HOSTNAME.EXE").read().strip()
if os.name == "posix":
    hostname = os.popen("/usr/bin/hostname").read().strip()
lastCPU = None # for some reason sometimes wmic cpu get loadpercentage fails to provide the cpu percentage so ima just send the last cpu percentage if that happens
def checkcpu():
    global lastCPU
    if os.name == "nt":
        cpuOutput = os.popen("wmic cpu get loadpercentage").read().strip()
        if cpuOutput == "LoadPercentage":
            return lastCPU + "%"
        else:
            lines = cpuOutput.splitlines()
            cpu = lines[2].strip()
            lastCPU = cpu
            return cpu + "%"
    if os.name == "posix":
        cpu = os.popen("/usr/bin/top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").read().strip()
        cpu = cpu[:-2] #remove the .x percent because the windows command doesn't have it & a discreptency would look ugly
        return cpu + "%"

def checkram():
    if os.name == "nt":
        output = os.popen("wmic os get FreePhysicalMemory,TotalVisibleMemorySize /Value")
        lines = [line.strip() for line in output if line.strip()]
        freeMemory = int(lines[0].split('=')[1])
        totalMemory = int(lines[1].split('=')[1])
        inUseMemory = totalMemory - freeMemory
        #convert to gb
        inUseMemory = inUseMemory/1048576
        totalMemory = totalMemory/1048576
        #gotta round it or it's stupidly long
        inUseMemory = round(inUseMemory, 1)
        totalMemory = round(totalMemory, 1)
        return str(inUseMemory) + "/" + str(totalMemory) + "GB"
    if os.name == "posix":
        output = os.popen("/usr/bin/free").read().strip()
        lines = output.split('\n')
        mem_line = lines[1].split()
        totalMemory = int(mem_line[1])
        inUseMemory = int(mem_line[2])
        #convert to gb
        totalMemory = totalMemory/1048576
        inUseMemory = inUseMemory/1048576
        #round
        totalMemory = round(totalMemory, 1)
        inUseMemory = round(inUseMemory, 1)
        return str(inUseMemory) + "/" + str(totalMemory) + "GB"


def start_client():
    host = ip
    port = port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

        
    while True:
        message = (hostname + " " + checkcpu() + " " + checkram())
        client_socket.send(message.encode())

            
        response = client_socket.recv(1024).decode()
        time.sleep(1)


if __name__ == "__main__":
    start_client()
