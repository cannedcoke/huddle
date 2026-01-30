import socket 
HOST = '192.168.20.67'
PORT = 9090 #importante tener el mismo puesto en el servidor y el cliente
# This line of code is creating a new socket object named `server` using the `socket.socket()` constructor. The `socket.socket()` function takes two arguments: the address family (in this case `socket.AF_INET` which indicates IPv4) and the socket type (in this case `socket.SOCK_STREAM` which indicates a TCP socket).
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST,PORT))

server.listen(5)#how many un accepted connections we alow before we reyect new ones
                #if more than 5 connections are waiti9ng we reyect the incoming ones
while True:
    # The line `communication_socket, address = server.accept()` is accepting an incoming connection on the server socket. When a client tries to connect to the server, the `accept()` method blocks and waits until a connection is established. Once a connection is made, it returns a new socket object representing the connection (communication_socket) and the address of the client (address).
    # communication_socket is what we use to talk to the individual client
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    # The line `message = communication_socket.recv(1024)` is reading data from the client connected to the server.
    message = communication_socket.recv(1024).decode('utf-8')
    print(f"the message is: {message}")
    
    communication_socket.send(f"recived, this coud've been an email".encode('utf-8'))
    communication_socket.close()
    print(f"connection with {address} ended ")
