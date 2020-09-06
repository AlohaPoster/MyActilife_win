import os
from socket import *
from time import ctime

HOST = ''  
PORT = 9733  
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
    filename = data.decode("utf-8")

    if(os.path.exists(filename + ".csv")):
        os.remove(filename + ".csv")
    else:
        tcpCliSock.send("0".encode())
        continue
    
    if(os.path.exists(filename + ".pdf")):
        os.remove(filename + ".pdf")
    else:
        tcpCliSock.send("0".encode())
        continue

    if(os.path.exists(filename + "_"+"Y-axis.png")):
        os.remove(filename + "_"+"Y-axis.png")
    else:
        tcpCliSock.send("0".encode())
        continue

    if(os.path.exists(filename + "_"+"Z-axis.png")):
        os.remove(filename + "_"+"Z-axis.png")
    else:
        tcpCliSock.send("0".encode())
        continue

    if(os.path.exists(filename + "_"+"X-axis.png")):
        os.remove(filename + "_"+"X-axis.png")
    else:
        tcpCliSock.send("0".encode())
        continue
    
    if(os.path.exists(filename + "_"+"combined.png")):
        os.remove(filename + "_"+"combined.png")
    else:
        tcpCliSock.send("0".encode())
        continue
    
    tcpCliSock.send("file finish".encode())
    tcpCliSock.close()
tcpSerSock.close()