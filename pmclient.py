# Nicholas Wharton
# Secure Password Manager
# Main Client Driver Program
# 1/13/2024

import socket
import os
import hashlib
import tkinter
import sys
from Crypto.Cipher import AES
from Crypto.Util import Padding
from pmclientbuttons import button1Set
from pmclientbuttons import button2Set
from pmclientbuttons import button3Set
from pmclientbuttons import button4Set
from pmclientbuttons import processInfo
from pmclientbuttons import noButton
from pmclientbuttons import sub
from pmclientservices import addService
from pmclientservices import displayService


# !!if server_port is equal to 0 the program will sense
# flood ports 1024-60000 on server to discover which port
# the server program is listening on!!
server_ip = '10.0.2.6'  # Replace with the actual server IP address
server_port = 0  # Default Port (Use the same port number as the server)


if (len(sys.argv) == 2): #if port number is input as first argument
    server_port = int(sys.argv[1])
elif (len(sys.argv) == 3): #if server address and port number are input as second argument and first argument respectivly
    server_port = int(sys.argv[1])
    server_ip = int(sys.argv[2])


def yesButton(buttonVar, val, username, window):
    buttonVar.set(val)
    window.destroy()
    menu(username)

# !!if server_port is equal to 0 the program will sense
# flood ports 1024-60000 on server to discover which port
# the server program is listening on!!
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

            client_socket.close()
            print("Servers listening on port " + str(i))
            server_port = i
            break
        except:
            continue

#starting menu asking user to choose either logging into a preexisting account or creating a new one.
def loginOrCreate():
    window = tkinter.Tk()
    window.title("Password Manager")
    window.geometry(f"{400}x{600}")
    buttonVar = tkinter.BooleanVar()
    twoVar = tkinter.BooleanVar()
    exitVar = tkinter.BooleanVar()

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Label(window, text="Welcome To The Password Manager").pack(pady=3)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Button(window, text="Create a New Account", command=lambda: button1Set(buttonVar, twoVar, window)).pack(pady=5)
    tkinter.Button(window, text="Login To an Existing Account", command=lambda: button2Set(buttonVar, twoVar, window)).pack(pady=5)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Button(window, text="Exit", command=lambda: button3Set(exitVar, buttonVar, window)).pack(pady=5)

    window.wait_variable(buttonVar)

    if (exitVar.get() == True):
        exit()

    if (twoVar.get() == False):
        login()
    else:
        create()




#authenticate a users account credentials
def login():
    window = tkinter.Tk()
    window.title("Password Manager")
    window.geometry(f"{400}x{600}")

    buttonVar = tkinter.BooleanVar()
    exitVar = tkinter.BooleanVar()

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Label(window, text="Login To an Existing Account").pack(pady=3)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)

    tkinter.Label(window, text="Enter Username:").pack(pady=3)
    uInput = tkinter.Entry(window)
    uInput.pack(pady=10)
    tkinter.Label(window, text="Enter Password:").pack(pady=3)
    pInput = tkinter.Entry(window, show='*')
    pInput.pack(pady=10)


    button = tkinter.Button(window, text="Submit", command=lambda: processInfo(buttonVar))
    button.pack(pady=5)

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    button = tkinter.Button(window, text="Exit", command=lambda: button4Set(exitVar, buttonVar, window))
    button.pack(pady=5)

    window.wait_variable(buttonVar)

    if (exitVar.get() == True):
        exit()

    password = pInput.get()
    username = uInput.get()

    #hash the password the user input
    hashObject = hashlib.sha256()
    hashObject.update(password.encode('utf-8'))
    passhash = hashObject.hexdigest()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = "L " + username + " " + passhash
    client_socket.sendall(message.encode('utf-8'))

    data = client_socket.recv(1024).decode('utf-8')
    while not data:
        data = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {data}")

    client_socket.close()

    responsearr = data.split()

    if responsearr[1] == "Succsessful":
        window.destroy()
    else:
        window.destroy()
        username = loginOrCreate()
    menu(username)







#Create a new user account.
def create():
    window = tkinter.Tk()
    window.title("Password Manager")
    window.geometry(f"{400}x{600}")

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Label(window, text="Create a New Account").pack(pady=3)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)

    buttonVar = tkinter.BooleanVar()
    exitVar = tkinter.BooleanVar()

    tkinter.Label(window, text="Enter Username:").pack(pady=3)
    uInput = tkinter.Entry(window)
    uInput.pack(pady=10)
    tkinter.Label(window, text="Enter Password:").pack(pady=3)
    pInput = tkinter.Entry(window, show='*')
    pInput.pack(pady=10)


    button = tkinter.Button(window, text="Submit", command=lambda: processInfo(buttonVar))
    button.pack(pady=5)

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    button = tkinter.Button(window, text="Exit", command=lambda: button4Set(exitVar, buttonVar, window))
    button.pack(pady=5)

    window.wait_variable(buttonVar)

    if (exitVar.get() == True):
        exit()

    username = uInput.get()
    password = pInput.get()

    if len(username) == 0 or len(password) == 0:
        window.destroy()
        create()
        exit()

    #hash the recieved password
    hashObject = hashlib.sha256()
    hashObject.update(password.encode('utf-8'))
    passhash = hashObject.hexdigest()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = "C " + username + " " + passhash
    client_socket.sendall(message.encode('utf-8'))

    data = client_socket.recv(1024).decode('utf-8')
    while not data:
        data = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {data}")

    client_socket.close()

    responsearr = data.split()

    if responsearr[1] == "Succsessfully":
        window.destroy()
    #start the menu for the users password manager
    else:
        window.destroy()
        loginOrCreate()
    menu(username)





#displays the users services, and another option to add a new service
def menu(username):
    print("ran")
    window = tkinter.Tk()
    window.title("Password Manager")
    window.geometry(f"{400}x{600}")

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Label(window, text="What Would You Like To Do?").pack(pady=3)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = "M " + username
    client_socket.sendall(message.encode('utf-8'))
    print("Sending: " + message)

    data = client_socket.recv(1024).decode('utf-8')
    while not data:
        data = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {data}")

    client_socket.close()

    responsearr = data.split()

    i = 0
    for service in responsearr:
        if service != "S":
            tkinter.Label(window, text=str(i) + ". " + service).pack(pady=3)
        i += 1

    tkinter.Label(window, text=str(i) + ". " + "Add a New Password\n").pack(pady=3)

    exitVar = tkinter.BooleanVar()

    #i = 1

    buttonVar = tkinter.BooleanVar()

    tkinter.Label(window, text="Enter #:").pack(pady=3)
    uInput = tkinter.Entry(window)
    uInput.pack(pady=10)

    button = tkinter.Button(window, text="Submit", command=lambda: processInfo(buttonVar))
    button.pack(pady=5)

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    button = tkinter.Button(window, text="Exit", command=lambda: button4Set(exitVar, buttonVar, window))
    button.pack(pady=5)

    window.wait_variable(buttonVar)

    if(exitVar.get() == True):
        window.destroy()
        exit()

    option = uInput.get()

    if len(option) == 0:
        window.destroy()
        menu(username)
        exit()

    if option.isdigit() == False:
        window.destroy()
        menu(username)
        exit()

    if int(option) < 1 or int(option) > i:
        window.destroy()
        menu(username)
        exit()


    #call addService() if the user selects to create a new service entry
    #if not attempt to display the service chosen by calling displaySerice()
    if int(option) == i:
        window.destroy()
        addService(username, server_ip, server_port)
    elif int(option) > 0 and int(option) < i:
        window.destroy()
        displayService(username, option, server_ip, server_port)

    #determine if the user wants to return to the passwork manager menu or exit
    window = tkinter.Tk()
    window.title("Password Manager")
    window.geometry(f"{400}x{600}")
    buttonVar = tkinter.BooleanVar()
    exitVar = tkinter.BooleanVar()

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Label(window, text="Would you like to continue using the manager?").pack(pady=3)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Button(window, text="Yes", command=lambda: yesButton(buttonVar, True, username, window)).pack(pady=5)
    tkinter.Button(window, text="No", command=lambda: noButton(buttonVar, True, window, exitVar)).pack(pady=5)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)

    window.wait_variable(buttonVar)



def main():
    #if server_port is not explicitly set in the code, or not input as an argument flood the servers ports to find the port its listening on.
    if server_port == 0:
        floodServer()
    print(server_port)
    loginOrCreate()

if __name__ == "__main__":
    main()
