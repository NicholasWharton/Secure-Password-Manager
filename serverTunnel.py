# Nicholas Wharton
# Secure Password Manager
# Server with single session and message encryption
# 2/28/2024

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import socket
import csv
import os
import hashlib
import sys
import tkinter
import threading
from Crypto.Cipher import AES
from Crypto.Util import Padding
from handleClients import HandleClient


#only needs to get client private key so it can share symmetric key securly
def shareSymmetricKey(conn):

    #used to read in the discover message
    discoverMsg = conn.recv(1024).decode('utf-8')
    while not discoverMsg:
        discoverMsg = conn.recv(1024).decode('utf-8')
    print("Received Inital Response From Client")

    #make sure the client is attempting to find this service on the server
    if discoverMsg == "Discover": #used for client to discover server
        print("Sent: Alive")
        conn.sendall("Alive".encode('utf-8'))
    else:
        exit()

    #now used to recieve the clients public key
    clientsPublicKey = conn.recv(1024)
    while not clientsPublicKey:
        clientsPublicKey = conn.recv(1024)
    print("Received Clients Public Key")

    cPublicKey = serialization.load_pem_public_key(clientsPublicKey, backend=default_backend())

    #genereate symmetric key
    symmKey = os.urandom(32)
    print("Generated Symmetric Key")

    # Encrypt a message using the public key
    encryptedSymmKey = cPublicKey.encrypt(
        symmKey,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

    #send client the encrypted symmetric key
    conn.sendall(encryptedSymmKey)
    print("Sent Client Encrypted Symmetric Key")

    HandleClient(conn, symmKey)




def main():
    if not os.path.isfile('users.csv'):
        with open('users.csv', 'w') as file:
            pass

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = socket.gethostname() # Bind to all available interfaces
    host = '0.0.0.0' # Bind to all available interfaces
    port = 5003  # Choose a port number

    if (len(sys.argv) == 2):
        port = int(sys.argv[1])

    server_socket.bind((host, port))

    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        shareSymmetricKey(conn)


if __name__ == "__main__":
    main()
