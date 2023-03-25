import threading
import socket

host = '127.0.0.1' # localhost
port = 55555 # unreserved port number

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen() # setting server in listining mode

clients = []
nicknames = []

# A function meant to broad cast a message to all the clients in the network
def broadcast(message):
    for client in clients:
        client.send(message)

def handel(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message) # broadcast the message to all the clients
        except:
            index = clients.index(client) # in case of exception 
            client.remove(client) # remove the client from the list
            client.close() # terminate the client connection
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat...'.encode('ascii')) # notify other clients that this client has left
            nicknames.remove(nickname) # remove the client's name from the list
            break

# A function meant to recieve client connection requests
def recieve():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}') # Notify that a client has successfuly connected with the server

        client.send('PING'.encode('ascii')) # send a request to the client requesting it's name
        nickname = client.recv(1024).decode('ascii') # decode the message sent back form client
        nicknames.append(nickname) # append the nickname ito the list
        clients.append(client) # append the clientr into the client list

        print(f'Nickname of client is {nickname}!') # Displays the nickname of the connected server
        broadcast(f'{nickname} joined the chat!'.encode('ascii')) # Broadcast the nickname of the client to other clients of the server
        client.send('Connected to the server'.encode('ascii')) # Sends back a confermation that the client the client has connected successfuly

        thread = threading.Thread(target=handel, args=(client,)) # Createing threads to manage multiple client interactions 
        thread.start()

print('Surver is up and running...!')
recieve()