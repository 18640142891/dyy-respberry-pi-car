import socket
import time
import sys

HOST = '192.168.137.1'
PORT = 8002
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

while True:
    connection, address = sock.accept()
    Building_connection = connection.recv(1024)
    if Building_connection == b"request":
        print("connection is ok!")
        connection.send(b'welcome to server!')  # 服务器已经连接

    while Building_connection == b"request":
        a = connection.recv(1024)  # 循环，持续通讯接收数据
        if a == b"exit":
            connection.send(b"close")
            break
        if a != b"request" and a:
            print("接收端:")
            print((a).decode())
            print("服务端：")
            se = input()
            connection.send((se).encode("utf-8"))
            print("")

    break
    connection.close()
    print("连接关闭")