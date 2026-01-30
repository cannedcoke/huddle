import socket
import threading


# direccion para el servidor
HOST = '192.168.20.67'
PORT = 9090

nick = input("choose a nickname: ")


# creo el socket del cliente y creo una conexión TCP con el servidor
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))


# intenta recibir constantemente datos, maneja errores, manda el nickname si es pedido
def recive():
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            message = message.decode('utf-8')
            
            if message == 'NICK':
                client.send(nick.encode('utf-8'))
            else:
                print(message)
        except:
            print("an error ocurred")
            client.close()
            break

# constantemente intenta mandar mensajes
def write():
    while True:
        try:
            msg = input("")
            from datetime import datetime
            now = datetime.now()
            message = f'{nick} {now.strftime("%H:%M")}: {msg}'
            client.send(message.encode('utf-8'))
        except:
            break
        
# uso threads para enviar y recibir mensajes al mismo tiempo sin bloquear el programa
recive_thread = threading.Thread(target=recive)
recive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()