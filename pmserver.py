# Nicholas Wharton
# Secure Password Manager
# Main Server Driver Function
# 1/13/2024

import socket
import csv
import os
import hashlib
import sys
import tkinter
import threading
from Crypto.Cipher import AES
from Crypto.Util import Padding

def HandleClient (conn, addr):
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received data: {data}")

        responsearr = data.split()

        if responsearr[0] == "Discover": #used for client to discover server
            conn.sendall("Alive".encode('utf-8'))

        elif responsearr[0] == "L": #user attempts to login
            username = responsearr[1]
            passhash = responsearr[2]
            found = False
            with open('users.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if username in row:
                        if passhash in row:
                            found = True
            if found == True:
                conn.sendall("Login Succsessful".encode('utf-8'))
            else:
                conn.sendall("Login Failed".encode('utf-8'))

        elif responsearr[0] == "C": #user attempts to create an account
            #check to see if the username is already taken.
            #if so rerun create()
            found = False
            username = responsearr[1]
            passhash = responsearr[2]
            with open('users.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if username in row:
                        found = True

            #save the new users name and password hash to the users file
            with open('users.csv', 'a') as file:
                writer = csv.writer(file)
                data = [username, passhash]
                writer.writerow(data)

            userfile = username + ".csv"
            #make sure the users file exists
            if not os.path.isfile(userfile):
                with open(userfile, 'w') as file:
                    pass

            if found == False:
                conn.sendall("Account Succsessfully Created".encode('utf-8'))
            else:
                conn.sendall("Account Creation Failed".encode('utf-8'))

        elif responsearr[0] == "M":
            username = responsearr[1]
            serviceString = "S "
            print("here")
            userfile = username + ".csv"
            with open(userfile, 'r') as file:
                reader = csv.reader(file)
                i = 0
                for row in reader:
                    serviceString += (row[0] + " ")
                    i += 1

            print("ServiceString:" + serviceString)
            conn.sendall(serviceString.encode('utf-8'))

        elif responsearr[0] == "AS":
            sInput = responsearr[1]
            uInput = responsearr[2]
            hexct = responsearr[3]
            keyhash = responsearr[4]

            username = responsearr[5]
            userfile = username + ".csv"

            data = [sInput, uInput, hexct, keyhash]

            with open(userfile, 'a') as file:
                writer = csv.writer(file)
                writer.writerow(data)

            conn.sendall("Service Added Succsessfully".encode('utf-8'))

        elif responsearr[0] == "DS":
            username = responsearr[1]
            keyhash = responsearr[2]

            readService = ""
            readUname = ""
            readPass = ""
            userfile = username + ".csv"

            with open(userfile, 'r') as file:
                reader = csv.reader(file)
                #if the key hash generated is the same as the one saved in the service entry
                for row in reader:
                    if keyhash == row[3]:
                        #decrypt the password and print the service information
                         readService = row[0]
                         readUname = row[1]
                         readPass = row[2]
                         break

            conn.sendall((readService + " " + readUname + " " + readPass).encode('utf-8'))

    conn.close()


def main():
    #make sure the users file exists
    if not os.path.isfile('users.csv'):
        with open('users.csv', 'w') as file:
            pass

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = socket.gethostname() # Bind to all available interfaces
    host = '0.0.0.0' # Bind to all available interfaces
    port = 12356  # Choose a port number

    if (len(sys.argv) == 2):
        port = int(sys.argv[1])

    server_socket.bind((host, port))

    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_thread = threading.Thread(target=HandleClient, args=(conn, addr))
        client_thread.start()


if __name__ == "__main__":
    main()
