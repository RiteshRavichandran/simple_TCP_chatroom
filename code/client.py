import socket
import threading

nickname = input('Choose a Nickname:\n') # User can enter a nickname for the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555)) # used to establish a connection to the server

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii') # recieves an encoded message from the server
            if message == 'PING': # If the message is 'PING' then the client sends its nickname to the server
                client.send(nickname.encode('ascii'))
            else:
                print(message) # prints the message sent by the server
        except:
            print('An error encountered!')
            client.close() # if an exception has accured then the client shall terminate itself
            break

def write():
    while True:
        message = f'{nickname}: {input("")}' # the client can take a message from the user
        client.send(message.encode('ascii')) # send the message to the server

receive_thread = threading.Thread(target = receive)
receive_thread.start() # Initiate revceive thread

write_thread = threading.Thread(target = write)
write_thread.start() # Initiate write thread