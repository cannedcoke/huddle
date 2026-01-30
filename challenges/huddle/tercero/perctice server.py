import socket
import threading

HOST = '192.168.20.67'
PORT = 9090

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
        
def remove(client):
    if client not in clients:
        return
    
    index = clients.index(clients)
    nick = nicknames[index]
    
    try:
        client.send('you left')
    except:
        pass
    
    
    clients.remove(client)
    nicknames.remove(nick)
    client.close()
    broadcast(f'{nick} left')
    

def handle(client):
    while True:
        try:
            try:
                message = client.recv(1024) 
                if not message:
                    break
            except OSError:
                remove(client)
                break
            message = message.decode('utf-8').strip()
            if message.endswith('/exit'):
                remove(client)
                break
            broadcast(message)
        except:
            remove(client)
            break
            
                
        

def recive():
    while True:
        client, adress = server.accept()
        client.send('NICK'.encode('utf-8'))
        nick = client.recv(1024).decode('utf-8')
        print(f"connection established witth {str(adress)}")
        broadcast(f"{nick} joined the chat! ")
        nicknames.append(nick)
        clients.append(client)
        
        thread= threading.Thread(target=handle,args=client,)
        thread.start()
        
        
print("server is listerning")
recive()
    