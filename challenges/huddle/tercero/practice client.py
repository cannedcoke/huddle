import threading
import socket

HOST = '192.168.20.67'#esta es mi ip local que el servidor va a usar para conectarse
PORT = 9090 

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

nick = input("enter a nickname")

def recive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            if message == 'NICK':
                client.send(nick.encode('utf-8'))
            else:
                print(message)
        except:
            print("somethings off")
            client.close()
            break
        
def write():
    while True:
        try:
            msg = input("")
            client.send(msg.encode('utf-8'))
        except:
            break

thread_send = threading.Thread(target=recive)