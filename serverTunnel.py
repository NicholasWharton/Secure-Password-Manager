# Nicholas Wharton
# Secure Password Manager
# Server with single session and message encryption
# 2/27/2024

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



#only needs to get client private key so it can share symmetric key securly
def shareSymmetricKey(conn):

    #used to read in the discover message
    data = conn.recv(1024).decode('utf-8')
    while not data:
        data = conn.recv(1024).decode('utf-8')
    print(f"Received response: {data}")

    if data == "Discover": #used for client to discover server
        print("Sent: Alive")
        conn.sendall("Alive".encode('utf-8'))

    #now used to recieve the clients public key
    data = conn.recv(1024).decode('utf-8')
    while not data:
        data = conn.recv(1024).decode('utf-8')
    print(f"Received response: {data}")





#def handleClient(symmetricKey):





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
