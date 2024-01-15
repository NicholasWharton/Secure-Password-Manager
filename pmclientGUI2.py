# Nicholas Wharton
# Secure Password Manager
# Main Client Driver Program
# 1/14/2024

import tkinter as tk
import socket
import os
import hashlib
import tkinter
import sys
from Crypto.Cipher import AES
from Crypto.Util import Padding


server_ip = '10.0.2.6'  # Replace with the actual server IP address
server_port = 5933
gusername = "nick"


class loginOrCreatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


    def update(self):
        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="What Would You Like To Do?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Button(self, text="Create a New Account", command=self.createAccount).grid(row=3, column=0)
        tk.Button(self, text="Login to Exiting Account", command=self.loginAccount).grid(row=4, column=0)
        tk.Button(self, text="Quit", command=self.quit).grid(row=5, column=0)

    def createAccount(self):
        self.controller.show_frame(CreatePage)

    def loginAccount(self):
        self.controller.show_frame(LoginPage)

    def quit(self):
        self.controller.quit()





class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = tk.StringVar()
        self.password = tk.StringVar()

    def update(self):
        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Login to an Existing Account?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text="Username:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.username).grid(row=4, column=0)
        tk.Label(self, text="Password:").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=6, column=0)

        tk.Button(self, text="Login", command=self.login).grid(row=7, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=8, column=0)

    def login(self):
        global gusername
        username = self.username.get()
        password = self.password.get()
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
        gusername = username

        if responsearr[1] == "Succsessful":
            self.controller.show_frame(MenuPage)
        else:
            self.controller.show_frame(loginOrCreatePage)

    def quit(self):
        self.controller.quit()






class CreatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = tk.StringVar()
        self.password = tk.StringVar()

    def update(self):
        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Create a New Account?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text="Username:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.username).grid(row=4, column=0)
        tk.Label(self, text="Password:").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=6, column=0)

        tk.Button(self, text="Create Account", command=self.createAccount).grid(row=7, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=8, column=1)

    def createAccount(self):
        global gusername
        username = self.username.get()
        password = self.password.get()

        if len(username) == 0 or len(password) == 0:
            self.controller.show_frame(loginOrCreatePage)

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
        gusername = username

        if responsearr[1] == "Succsessfully":
            self.controller.show_frame(MenuPage)
        else:
            self.controller.show_frame(loginOrCreatePage)

    def quit(self):
        self.controller.quit()




class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numInput = tk.StringVar()
        self.i = 0

    def update(self):
        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="What Would You Like To Do?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        message = "M " + gusername
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
                tk.Label(self, text=str(i) + ". " + service).grid(row=(i+2), column=0)
            i += 1

        tk.Label(self, text=str(i) + ". " + "Add a New Password\n").grid(row=(i+2), column=0)

        tk.Label(self, text="Enter #:").grid(row=(i+3), column=0)
        tk.Entry(self, textvariable=self.numInput).grid(row=(i+3), column=1)

        self.i = i

        tk.Button(self, text="Submit", command=self.submit).grid(row=(i+4), column=0)

        tk.Button(self, text="Quit", command=self.quit).grid(row=(i+5), column=0)

    def submit(self):
        self.controller.show_frame(loginOrCreatePage)
        selectedOption = self.numInput.get()
        i = self.i
        print(self.i)

        if int(selectedOption) == i:
            self.controller.show_frame(AddServicePage)
        elif int(selectedOption) < i and int(selectedOption) >= 0:
            #self.controller.show_frame(displayService)
            print("Hi")
        else:
            self.controller.show_frame(MenuPage)

    def quit(self):
        self.controller.quit()





class AddServicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.service = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.key = tk.StringVar()

    def update(self):
        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Login to an Existing Account?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text="Service:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.service).grid(row=4, column=0)
        tk.Label(self, text="Username:").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.username).grid(row=6, column=0)
        tk.Label(self, text="Password:").grid(row=7, column=0)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=8, column=0)
        tk.Label(self, text="Key (16 bytes):").grid(row=9, column=0)
        tk.Entry(self, textvariable=self.key, show="*").grid(row=10, column=0)

        tk.Button(self, text="Login", command=self.addService).grid(row=11, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=12, column=0)

    def addService(self):
        service = self.service.get()
        username = self.username.get()
        password = self.password.get()
        key = self.key.get()

        if len(service) == 0 or len(username) == 0 or len(password) == 0 or len(key) != 16:
            self.controller.show_frame(AddServicePage)
            return

        if len(key) != 16:
            self.controller.show_frame(AddServicePage)
            return

        #Clear the page
        for widget in self.winfo_children():
            widget.place_forget()

        #get the hash of the inputted key to compare it with the saved key hash
        hashObject = hashlib.sha256()
        hashObject.update(key.encode('utf-8'))
        keyhash = hashObject.hexdigest()

        #encrypt the password with the given key
        cipher = AES.new(key.encode(), AES.MODE_CBC, b'\x00' * AES.block_size)
        paddedPlain = Padding.pad(password.encode(), AES.block_size)
        ciphertext = cipher.encrypt(paddedPlain)

        #Save the service name, the user name for the service, the encrypted
        #password, and a hash of the key to the users service file.
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        message = "AS " + service + " " + username + " " + ciphertext.hex() + " " + keyhash + " " + username
        client_socket.sendall(message.encode('utf-8'))

        data = client_socket.recv(1024).decode('utf-8')
        while not data:
            data = client_socket.recv(1024).decode('utf-8')
        print(f"Received response: {data}")

        client_socket.close()

    def quit(self):
        self.controller.quit()








class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (AddServicePage, LoginPage, CreatePage, MenuPage, loginOrCreatePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(loginOrCreatePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()

if __name__ == "__main__":
    app = Application()
    app.geometry("300x600")
    app.mainloop()
