import os
from socket import *
from time import ctime

HOST = ''  
PORT = 9779  
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
    print("recv:",data.decode("utf-8"))
    if not data:
        tcpCliSock.close()
        continue
    filename = data.decode("utf-8")
    if os.path.exists(filename):
        filesize = str(os.path.getsize(filename))
        print("size:",filesize)
        tcpCliSock.send(filesize.encode())
        data = tcpCliSock.recv(BUFSIZ)   
        print("begin")
        f = open(filename, "rb")
        for line in f:
            tcpCliSock.send(line)
        data = tcpCliSock.recv(BUFSIZ)
    else:
        tcpCliSock.send("0001".encode())
    print("closing.....")   
    tcpCliSock.close()
tcpSerSock.close()