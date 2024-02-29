# Nicholas Wharton
# Secure Password Manager
# Main Server Handeling Client Requests after the tunnel establishment is completed
# 2/28/2024


import csv
import socket
from Crypto.Cipher import AES
from Crypto.Util import Padding

def HandleClient (conn, symmetricKey):

    while True:
        data = conn.recv(1024)
        if not data:
            break
        cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
        dec = cipher.decrypt(data)
        pplain = Padding.unpad(dec, AES.block_size).decode()
        print(f"Received response: {pplain}")

        responsearr = pplain.split()

        if responsearr[0] == "L": #user attempts to login
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
                print("Sent: Login Succsessful")

                message = "Login Succsessful"
                cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
                paddedPlain = Padding.pad(message.encode(), AES.block_size)
                ciphertext = cipher.encrypt(paddedPlain)
                conn.sendall(ciphertext)

            else:
                print("Sent: Login Failed")

                message = "Login Failed"
                cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
                paddedPlain = Padding.pad(message.encode(), AES.block_size)
                ciphertext = cipher.encrypt(paddedPlain)
                conn.sendall(ciphertext)

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
                print("Sent: Account Succsessfully Created")

                message = "Account Succsessfully Created"
                cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
                paddedPlain = Padding.pad(message.encode(), AES.block_size)
                ciphertext = cipher.encrypt(paddedPlain)
                conn.sendall(ciphertext)

            else:
                print("Sent: Account Creation Failed")

                message = "Account Creation Failed"
                cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
                paddedPlain = Padding.pad(message.encode(), AES.block_size)
                ciphertext = cipher.encrypt(paddedPlain)
                conn.sendall(ciphertext)

        elif responsearr[0] == "M":
            username = responsearr[1]
            serviceString = "S "
            userfile = username + ".csv"
            with open(userfile, 'r') as file:
                reader = csv.reader(file)
                i = 0
                for row in reader:
                    serviceString += (row[0] + " ")
                    i += 1

            print("ServiceString:" + serviceString)
            message = "Account Creation Failed"
            cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
            paddedPlain = Padding.pad(serviceString.encode(), AES.block_size)
            ciphertext = cipher.encrypt(paddedPlain)
            conn.sendall(ciphertext)

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
                print("Sent: Service Added Succsessfully")

                message = "Service Added Succsessfully"
                cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
                paddedPlain = Padding.pad(message.encode(), AES.block_size)
                ciphertext = cipher.encrypt(paddedPlain)
                conn.sendall(ciphertext)

        elif responsearr[0] == "DS":
            username = responsearr[1]
            keyhash = responsearr[2]
            service = responsearr[3]

            readUname = ""
            readPass = ""
            userfile = username + ".csv"

            with open(userfile, 'r') as file:
                reader = csv.reader(file)
                #if the key hash generated is the same as the one saved in the service entry
                for row in reader:
                    if service == row[0] and keyhash == row[3]:
                        #decrypt the password and print the service information
                         readUname = row[1]
                         readPass = row[2]
                         break

            if readUname == "":
                print("Sent: Key Invalid")

                message = "Key Invalid"
                cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
                paddedPlain = Padding.pad(message.encode(), AES.block_size)
                ciphertext = cipher.encrypt(paddedPlain)
                conn.sendall(ciphertext)

            else:
                print("Sent: Key Valid")
                message = service + " " + readUname + " " + readPass
                cipher = AES.new(symmetricKey, AES.MODE_CBC, b'\x00' * AES.block_size)
                paddedPlain = Padding.pad(message.encode(), AES.block_size)
                ciphertext = cipher.encrypt(paddedPlain)
                conn.sendall(ciphertext)
