# Nicholas Wharton
# Secure Password Manager
# Client with single session and message encryption
# 2/27/2024

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import tkinter as tk
import socket
import os
import hashlib
import tkinter
import sys
from Crypto.Cipher import AES
from Crypto.Util import Padding

server_ip = '10.0.2.6'
server_port = 0


def floodServer():
    global server_port
    for i in range(1024, 60000):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, i))
            message = "Discover"
            client_socket.sendall(message.encode('utf-8'))

            data = client_socket.recv(1024).decode('utf-8')
            while not data:
                data = client_socket.recv(1024).decode('utf-8')
            print(f"Received response: {data}")

            print("Servers listening on port " + str(i))
            server_port = i
            break
        except:
            continue

    GenerateSessionKey(client_socket)


#Generates the Public and Private Key to securly share a symmetric key to use for the rest of the session
def GenerateSessionKey(client_socket):
    privateSessionKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    publicSessionKey = privateSessionKey.public_key()
    shareSessionPublicKey(client_socket, privateSessionKey, publicSessionKey)


#Shares the Public and Private Key to the server securly share a symmetric key to use for the rest of the session
def shareSessionPublicKey(client_socket, privateSessionKey, publicSessionKey):

    publicKeyBytes = publicSessionKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    client_socket.sendall(publicKeyBytes)
    print("Sent Public Session Key to Server")






floodServer()


# # Encrypt a message using the public key
# message = b"Hello, this is a secret message."
# encrypted_message = public_key.encrypt(
#     message,
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()),
#         algorithm=hashes.SHA256(),
#         label=None
#     )
# )
#
# # Decrypt the message using the private key
# decrypted_message = private_key.decrypt(
#     encrypted_message,
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()),
#         algorithm=hashes.SHA256(),
#         label=None
#     )
# )
#
# print("Original message:", message)
# print("Decrypted message:", decrypted_message)

    # # Serialize the public key to PEM format
    # serialPK = publicSessionKey.public_bytes(
    #     encoding=serialization.Encoding.PEM,
    #     format=serialization.PublicFormat.SubjectPublicKeyInfo
    # )
    #
    # # Convert bytes to ASCII string
    # asciiPK = serialPK.decode('ascii')
    # message = "newconn " + asciiPK
