# Nicholas Wharton
# Secure Password Manager
# Client with single session and message encryption
# 2/28/2024

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import tkinter as tk
import socket
import os
import sys
from clientMenu import loginOrCreatePage, MenuPage, CreatePage, LoginPage, AddServicePage, ContinuePage, DisplayServicePage


#floods server ports with discover message until it connects to the server port and recieves a response
def floodServer():
    server_ip = '10.0.2.6' #servers ip address
    server_port = 0 #servers default port number

    #check all ports from 1024 - 60000
    for i in range(1024, 60000):
        #attempt to connect to the port
        try:
            #create the connection
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((server_ip, i))

            #form the discover message and send it over the connection
            message = "Discover"
            clientSocket.sendall(message.encode('utf-8'))

            #wait for response from the server
            data = clientSocket.recv(1024).decode('utf-8')
            while not data:
                data = clientSocket.recv(1024).decode('utf-8')
            print(f"Received response: {data}")

            #if a response is recived you have found the correct port and continue to the key exchange
            print("Servers listening on port " + str(i))
            server_port = i
            break
        #if the connection fails continue to connect to the next port number
        except:
            continue

    #start the key excahge process
    symmetricKey = GenerateSessionKey(clientSocket)
    return symmetricKey, clientSocket




#Generates the Public and Private Key to securly share a symmetric key to use for the rest of the session
def GenerateSessionKey(clientSocket):
    #generate the private key
    privateSessionKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    #generate the public key based on the private key
    publicSessionKey = privateSessionKey.public_key()

    #start the key sharing process passing the generated keys and the connection
    symmetricKey = shareSessionPublicKey(clientSocket, privateSessionKey, publicSessionKey)
    return symmetricKey


#Shares the Public and Private Key to the server securly share a symmetric key to use for the rest of the session
def shareSessionPublicKey(clientSocket, privateSessionKey, publicSessionKey):

    #serialize the public key into bytes
    publicKeyBytes = publicSessionKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    #send public key to sever so it can encypt the symmetric key so it can only be
    #decrypted using the clients private key.
    clientSocket.sendall(publicKeyBytes)
    print("Sent Public Session Key to Server")

    #recieve the encrypted symmetric key from the server
    encryptedSymmetricKey = clientSocket.recv(1024)
    while not encryptedSymmetricKey:
        encryptedSymmetricKey = clientSocket.recv(1024)
    print("Received Encrypted Symmetric Key")

    # Decrypt the message using the private key
    symmetricKey = privateSessionKey.decrypt(
        encryptedSymmetricKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("Recieved Symmetric Key")
    return symmetricKey



#The application window parent class
class Application(tk.Tk):
    #initalization method for the application
    def __init__(self, *args, **kwargs):
        key = kwargs.pop('key') #the symmetric key that should be used to encrypt all messages in each frame
        clientSocket = kwargs.pop('clientSocket') #the client socket object to be used by each frame
        self.clientSocket = clientSocket #allows the onClose function to close the client socket when the application is closed with the x

        #initalizes the application window
        tk.Tk.__init__(self, *args, **kwargs)
        #used to control the applcation container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        #defines all of the windows for the application, and the information to pass to each
        self.frames = {}
        for F in (DisplayServicePage, ContinuePage, AddServicePage, LoginPage, CreatePage, MenuPage, loginOrCreatePage):
            frame = F(container, self, key, clientSocket)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #start the applciation on the loginOrCreatePage
        self.showFrame(loginOrCreatePage)

        #when the window is deleted run the onClose function
        self.protocol("WM_DELETE_WINDOW", self.onClose)

    #switch frames on the application window
    def showFrame(self, cont):
        #When a frame is switched to update the page before raising it to the top of the container so it can be viewed
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()

    #when the application window is closed
    def onClose(self):
        self.clientSocket.close()



#Start the program by finding which port the server is on then starting the key sharing process
def main():
    #get the symmetric key and socket connection object to pass to the applciation instance when its created
    symmetricKey, cs = floodServer()

    app = Application(key = symmetricKey, clientSocket = cs)
    app.geometry("500x600")
    app.mainloop()



if __name__ == "__main__":
    main()
