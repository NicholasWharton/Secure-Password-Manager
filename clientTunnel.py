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



def floodServer():
    server_ip = '10.0.2.6'
    server_port = 0

    for i in range(1024, 60000):
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((server_ip, i))
            message = "Discover"
            clientSocket.sendall(message.encode('utf-8'))

            data = clientSocket.recv(1024).decode('utf-8')
            while not data:
                data = clientSocket.recv(1024).decode('utf-8')
            print(f"Received response: {data}")

            print("Servers listening on port " + str(i))
            server_port = i
            break
        except:
            continue

    symmetricKey = GenerateSessionKey(clientSocket)
    return symmetricKey, clientSocket




#Generates the Public and Private Key to securly share a symmetric key to use for the rest of the session
def GenerateSessionKey(clientSocket):
    privateSessionKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    publicSessionKey = privateSessionKey.public_key()

    symmetricKey = shareSessionPublicKey(clientSocket, privateSessionKey, publicSessionKey)
    return symmetricKey


#Shares the Public and Private Key to the server securly share a symmetric key to use for the rest of the session
def shareSessionPublicKey(clientSocket, privateSessionKey, publicSessionKey):

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




class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        key = kwargs.pop('key')
        clientSocket = kwargs.pop('clientSocket')
        self.clientSocket = clientSocket

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (DisplayServicePage, ContinuePage, AddServicePage, LoginPage, CreatePage, MenuPage, loginOrCreatePage):
            frame = F(container, self, key, clientSocket)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(loginOrCreatePage)

        self.protocol("WM_DELETE_WINDOW", self.onClose)

    #switch frames on the application window
    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()

    #when the application window is closed
    def onClose(self):
        self.clientSocket.close()



#Start the program by finding which port the server is on then starting the key sharing process
def main():
    symmetricKey, cs = floodServer()

    app = Application(key = symmetricKey, clientSocket = cs)
    app.geometry("300x600")
    app.mainloop()



if __name__ == "__main__":
    main()
