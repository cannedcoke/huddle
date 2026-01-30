import threading 
import socket 
from colorama import init, Fore, Style
init()



HOST = '192.168.20.67'
PORT = 9090 

# creo el socket tcp ,lo instancio, genero cola de conexiones
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients = []
nicks = []

# permite que solo un hilo acceda a los recursos compartidos a la vez
lock = threading.Lock()


# intenta enviar un mensaje al cliente y lo elimina si falla varias veces
def broadcast(message):
    with lock:
        for client in clients:
            safe_send(client,message)
        

# maneja errores y envia mensajes a clientes individuales
def safe_send(client, message, retries=3):
    for _ in range(retries):
        try:
            client.send(message)
            return
        except:
            continue
    remove(client) 


# remueve a clientes de manera segura
def remove(client):
    with lock:
            if client not in clients:
                return
            
            index = clients.index(client)
            nick = nicks[index]
            
            try:
                txt = (Fore.RED + Style.BRIGHT + "You left the chat."+ Style.RESET_ALL)
                client.send(txt.encode('utf-8'))
            except:
                pass
            
            clients.remove(client)
            nicks.remove(nick)
            client.close()
            print(Fore.RED + Style.BRIGHT + f"{nick} has left the chat"+ Style.RESET_ALL)
    txt =(Fore.RED + Style.BRIGHT + f"{nick} left </3"+ Style.RESET_ALL)
    broadcast(txt.encode('utf-8'))

# recibe, valida , retransmite mensajes
def handle(client):
    while True:
        try:
      
            try:
                message = client.recv(1024)
                
                if not message:
                    remove(client)
                    break
                
            except OSError:
                remove(client)
                break


            text = message.decode('utf-8').strip()

           
            if text.endswith("/exit"):
                
                remove(client)
                break
            
            broadcast(message)
        except:
            remove(client)
            break



# acepta conexiones, guarda a los clientes, inicia un thread para correr una instancia por cliente
def receive():
    while True:

        client, address = server.accept()
        print(Fore.YELLOW + Style.BRIGHT + f"connected with {str(address)}"+ Style.RESET_ALL)
        client.send('NICK'.encode('utf-8'))
        nick = client.recv(1024).decode('utf-8')
        nicks.append(nick)
        clients.append(client)
        
        print(Fore.YELLOW + Style.BRIGHT + f"the nickname of the client is {nick}!"+ Style.RESET_ALL)
        txt =(Fore.YELLOW + Style.BRIGHT + f"{nick} is here... "+ Style.RESET_ALL)
        broadcast(txt.encode('utf-8'))
        txt =(Fore.LIGHTGREEN_EX + Style.BRIGHT + "connected to the server"+ Style.RESET_ALL)
        client.send(txt.encode('utf-8'))
        
        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
        

print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "server is listening... "+ Style.RESET_ALL)
receive()