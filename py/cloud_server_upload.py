import os
from socket import *
from time import ctime

HOST = ''  
PORT = 9711  
BUFSIZ = 1024  
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)  
tcpSerSock.bind(ADDR)  
tcpSerSock.listen(32)     

while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('...connected from:', addr)
    data = tcpCliSock.recv(BUFSIZ)
    myfile = "./cpat/" + data.decode("utf-8")
    if os.path.exists(myfile):
        pass
    else:
        os.makedirs(myfile)
    tcpCliSock.send("makedirs finish".encode())
    data = tcpCliSock.recv(BUFSIZ)
    print("path:",data.decode("utf-8"))
    if not data:
        tcpCliSock.close()
        continue
    filename = data.decode("utf-8")
    tcpCliSock.send("Filename received".encode())
    data = tcpCliSock.recv(BUFSIZ)
    file_total_size = int(data.decode())
    received_size = 0
    tcpCliSock.send("Filesize received".encode())
    f = open(filename,"wb")
    while received_size < file_total_size:
        data = tcpCliSock.recv(BUFSIZ)
        f.write(data)
        received_size += len(data)
    f.close()  
    tcpCliSock.send("file received".encode())
    tcpCliSock.close()
tcpSerSock.close()