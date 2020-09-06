#-*- coding:utf-8 -*-
"""
__author__ = BlingBling
"""
#!/usr/bin/env python

from socket import *
import os

HOST = '47.96.227.243'
PORT_get = 9779
PORT_send = 9711
PORT_del = 9720
BUFSIZ = 1024
ADDR_get = (HOST, PORT_get)
ADDR_send = (HOST, PORT_send)
ADDR_del = (HOST, PORT_del)

def deletesm(res):
    #rawdatapng_url,rawdatacsv_url,report_url,filename 
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR_del)
    tcpCliSock.send(bytes(res[0]+res[3], 'utf-8'))
    data = tcpCliSock.recv(BUFSIZ)
    if data.decode()=="0":
        return "unsuccessful"
    else:
        tcpCliSock.close()
        return "yes"

def getsm(result_id,localpath,serverpath,serverfilename):
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR_get)
    tcpCliSock.send(bytes(serverpath + serverfilename, 'utf-8'))
    data = tcpCliSock.recv(BUFSIZ)
    if not data:
        return 
    if data.decode() == "0001":
        return "noneexist"
    else:
        tcpCliSock.send("File size received".encode())
        file_total_size = int(data.decode())
        received_size = 0
        f = open(localpath + result_id +"_"+serverfilename,"wb")
        while received_size < file_total_size:
            data = tcpCliSock.recv(BUFSIZ)
            f.write(data)
            received_size += len(data)
            print("已接收:",received_size)
        f.close()
        tcpCliSock.send("file received".encode())
    tcpCliSock.close()

def sendsm(resultid,localpath,serverpath,serverfilename):
    filee = localpath + serverfilename
    if os.path.exists(filee):
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR_send)
        tcpCliSock.send(bytes("c" + resultid,"utf-8"))
        data = tcpCliSock.recv(BUFSIZ)
        tcpCliSock.send(bytes(serverpath + serverfilename, 'utf-8'))
        data = tcpCliSock.recv(BUFSIZ)
        filesize = str(os.path.getsize(filee))
        tcpCliSock.send(filesize.encode())
        data = tcpCliSock.recv(BUFSIZ)   
        f = open(filee, "rb")
        for line in f:
            tcpCliSock.send(line)
        data = tcpCliSock.recv(BUFSIZ)
    else:
        return "noneexist"
    tcpCliSock.close()
    
if __name__ == "__main__":
    sendsm("100","/Users/zhangruilin/Desktop/","./cpat/c100/","lowell.pdf")
# while True:
#     message = input('> ')
#     if not message:
#         break
#     tcpCliSock.send(bytes(message, 'utf-8'))
#     data = tcpCliSock.recv(BUFSIZ)
#     if not data:
#         break
#     if data.decode() == "0001":
#         print("Sorr file %s not found"%message)
#     else:
#         tcpCliSock.send("File size received".encode())
#         file_total_size = int(data.decode())
#         received_size = 0
#         f = open("new" + message  ,"wb")
#         while received_size < file_total_size:
#             data = tcpCliSock.recv(BUFSIZ)
#             f.write(data)
#             received_size += len(data)
#             print("已接收:",received_size)
#         f.close()
#         print("receive done",file_total_size," ",received_size)
# tcpCliSock.close()
