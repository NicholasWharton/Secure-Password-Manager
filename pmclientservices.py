import socket
import tkinter
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Padding
from pmclientbuttons import button4Set
from pmclientbuttons import processInfo
from pmclientbuttons import processInfo5

#adds a new service entry to the users services file.
def addService(username, server_ip, server_port):
    window = tkinter.Tk()
    window.title("Password Manager")
    window.geometry(f"{400}x{600}")
    buttonVar = tkinter.BooleanVar()
    exitVar = tkinter.BooleanVar()

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Label(window, text="Adding a New Service").pack(pady=3)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)

    tkinter.Label(window, text="Enter Service:").pack(pady=3)
    sInput = tkinter.Entry(window)
    sInput.pack(pady=10)
    tkinter.Label(window, text="Enter Username:").pack(pady=3)
    uInput = tkinter.Entry(window)
    uInput.pack(pady=10)
    tkinter.Label(window, text="Enter Password:").pack(pady=3)
    pInput = tkinter.Entry(window, show='*')
    pInput.pack(pady=10)
    tkinter.Label(window, text="Enter Key (16 Bytes):").pack(pady=3)
    kInput = tkinter.Entry(window)
    kInput.pack(pady=10)


    button = tkinter.Button(window, text="Submit", command=lambda: processInfo(buttonVar))
    button.pack(pady=5)

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    button = tkinter.Button(window, text="Exit", command=lambda: button4Set(exitVar, buttonVar, window))
    button.pack(pady=5)

    window.wait_variable(buttonVar)

    if exitVar.get() == True:
        window.destroy()
        exit()

    kInput = kInput.get()
    pInput = pInput.get()
    uInput = uInput.get()
    sInput = sInput.get()

    if len(sInput) == 0 or len(kInput) == 0 or len(uInput) == 0 or len(pInput) == 0:
        window.destroy()
        addService(username, server_ip, server_port)
        return

    if len(kInput) != 16:
        window.destroy()
        addService(username, server_ip, server_port)
        return

    window.destroy()

    #get the hash of the inputted key to compare it with the saved key hash
    hashObject = hashlib.sha256()
    hashObject.update(kInput.encode('utf-8'))
    keyhash = hashObject.hexdigest()

    #encrypt the password with the given key
    cipher = AES.new(kInput.encode(), AES.MODE_CBC, b'\x00' * AES.block_size)
    paddedPlain = Padding.pad(pInput.encode(), AES.block_size)
    ciphertext = cipher.encrypt(paddedPlain)

    #Save the service name, the user name for the service, the encrypted
    #password, and a hash of the key to the users service file.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = "AS " + sInput + " " + uInput + " " + ciphertext.hex() + " " + keyhash
    client_socket.sendall(message.encode('utf-8'))

    data = client_socket.recv(1024).decode('utf-8')
    while not data:
        data = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {data}")

    client_socket.close()




#displays the services information if the key used to encrypt the password is input
def displayService(username, option, server_ip, server_port):
    hashObject = hashlib.sha256()
    key = ""


    while len(key) != 16:
        window = tkinter.Tk()
        window.title("Password Manager")
        window.geometry(f"{400}x{600}")
        buttonVar = tkinter.BooleanVar()
        exitVar = tkinter.BooleanVar()

        tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
        tkinter.Label(window, text="Displaying a Service").pack(pady=3)
        tkinter.Label(window, text="-----------------------------------------").pack(pady=3)

        tkinter.Label(window, text="Enter 16 Byte Key: ").pack(pady=3)
        kInput = tkinter.Entry(window)
        kInput.pack(pady=10)

        button = tkinter.Button(window, text="Submit", command=lambda: processInfo5(buttonVar, window))
        button.pack(pady=5)

        tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
        button = tkinter.Button(window, text="Exit", command=lambda: button4Set(exitVar, buttonVar, window))
        button.pack(pady=5)

        window.wait_variable(buttonVar)
        key = kInput.get()
        window.destroy()

        if exitVar.get() == True:
            exit()

    #hash the inputted key
    hashObject.update(key.encode('utf-8'))
    keyhash = hashObject.hexdigest()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = "DS " + username + " " + keyhash
    client_socket.sendall(message.encode('utf-8'))

    data = client_socket.recv(1024).decode('utf-8')
    while not data:
        data = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {data}")

    client_socket.close()

    responsearr = data.split()

    cipher = AES.new(key.encode(), AES.MODE_CBC, b'\x00' * AES.block_size)
    dec = cipher.decrypt(bytes.fromhex(responsearr[2]))
    pplain = Padding.unpad(dec, AES.block_size).decode()

    window = tkinter.Tk()
    window.title("Password Manager")
    window.geometry(f"{400}x{600}")
    buttonVar = tkinter.BooleanVar()

    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)
    tkinter.Label(window, text="Displaying a Service").pack(pady=3)
    tkinter.Label(window, text="-----------------------------------------").pack(pady=3)

    tkinter.Label(window, text="Service: " + responsearr[0]).pack(pady=3)
    tkinter.Label(window, text="Username: " + responsearr[1]).pack(pady=3)

    tkinter.Label(window, text="Password: " + pplain).pack(pady=3)

    button = tkinter.Button(window, text="Close Menu", command=lambda: processInfo5(buttonVar, window))
    button.pack(pady=5)
    window.wait_variable(buttonVar)
    window.destroy()
