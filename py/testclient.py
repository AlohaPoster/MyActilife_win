#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from socket import *
import time

def client_sub(client_socket):
    """用户选择操作函数"""
    print("**" * 20)
    print("1:上传数据")
    print("2:下载数据")
    print("3:断开连接")
    client_pro = input("请选择你要的操作:")
    if client_pro == "1":
        client_socket.send(client_pro.encode('utf-8'))
        # 向服务器上传数据功能
        print("准备向服务器上传数据")
        send_file(client_socket)
    elif client_pro == "2":
        client_socket.send(client_pro.encode('utf-8'))
        # 从服务器下载数据
        print("准备从服务器下载数据")
        download_file(client_socket)
    elif client_pro == "3":
        client_socket.send(client_pro.encode('utf-8'))
        # 断开链接
        print("准备断开链接")
        client_socket.send("3".encode('utf-8'))
        client_socket.close()
        return "1"
    else:
        print("您输入的选项有误,请从新输入")
        client_sub(client_socket)

def send_file(client_socket):
    """客户端上传文件"""
    file_name = input("请输入您要上传的文件名")
    client_socket.send(file_name.encode("utf-8"))
    try:
        f = open(file_name,'rb')
    except Exception:
        print('没有此文件!')
    else:
        file_content = f.read(1024)
        f.close()
        client_socket.send(file_content)
        time.sleep(1)
        print("文件上传成功!")
        time.sleep(1)

def download_file(client_socket):
    """文件下载"""
    file_name = input("请输入您要下载的文件名")
    client_socket.send(file_name.encode("utf-8"))
    try:
        with open(file_name, "wb") as file:
            while True:
                file_data = client_socket.recv(1024)
                if file_data =='exit' or not file_data:
                    break
                else:
                    print("收到了1024")
                    file.write(file_data)
    except Exception as e:
        print("下载异常", e)
    else:
        print(file_name, "下载成功")

def main():
    """tcp客户端主程序"""
    client_socket = socket(AF_INET,SOCK_STREAM)
    server_ip = "47.96.227.243" 
    server_port = 9777
    client_socket.connect((server_ip,server_port))
    print("连接服务器成功!")
    while True:
        pro = client_sub(client_socket)
        if pro == "1":
            break


if __name__ == '__main__':
    main()
