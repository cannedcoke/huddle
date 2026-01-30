import socket

HOST = '192.168.20.67'
PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))#this sends a requet to the server with the designed port and host or ip adress

sock.send("we're done".encode('utf-8'))
print(sock.recv(1024).decode('utf-8'))
