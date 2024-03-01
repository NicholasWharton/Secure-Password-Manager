# Nicholas Wharton
# Secure Password Manager
# Main Client Driver Program
# 1/16/2024

import tkinter as tk
import socket
import os
import hashlib
import tkinter
import sys
from Crypto.Cipher import AES
from Crypto.Util import Padding


server_ip = '10.0.2.6'  # Replace with the actual server IP address
server_port = 0
gusername = "n"
gservice = "n"
gservicelist = "n"

if (len(sys.argv) == 2): #if port number is input as first argument
    server_port = int(sys.argv[1])
elif (len(sys.argv) == 3): #if server address and port number are input as second argument and first argument respectivly
    server_port = int(sys.argv[1])
    server_ip = int(sys.argv[2])



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


#Page to choose to login to an existing pm user account or create a new pm user account
class loginOrCreatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

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




#Page to login into an existing account
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = tk.StringVar()
        self.password = tk.StringVar()

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Login to an Existing Account?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text="Username:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.username).grid(row=4, column=0)
        tk.Label(self, text="Password:").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=6, column=0)

        tk.Button(self, text="Login", command=self.login).grid(row=7, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=8, column=0)

    #Once the user submits the login info
    def login(self):
        global gusername
        username = self.username.get()
        password = self.password.get()

        #generate password hash
        hashObject = hashlib.sha256()
        hashObject.update(password.encode('utf-8'))
        passhash = hashObject.hexdigest()

        #connect to the server and send the username and password hash to be authenticated
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

        #choose behavior based on server response
        if responsearr[1] == "Succsessful":
            self.controller.show_frame(MenuPage)
        else:
            self.controller.show_frame(loginOrCreatePage)

    def quit(self):
        self.controller.quit()





#Page used to create a new user account
class CreatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.passwordconf = tk.StringVar()

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.passwordconf = tk.StringVar()

        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Create a New Account?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text="Username:").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.username).grid(row=4, column=0)
        tk.Label(self, text="Password:").grid(row=5, column=0)
        tk.Entry(self, textvariable=self.password, show="*").grid(row=6, column=0)
        tk.Label(self, text="Confirm Password:").grid(row=7, column=0)
        tk.Entry(self, textvariable=self.passwordconf, show="*").grid(row=8, column=0)

        tk.Button(self, text="Create Account", command=self.createAccount).grid(row=9, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=10, column=0)

    #Once the user submits the account info
    def createAccount(self):
        global gusername
        username = self.username.get()
        password = self.password.get()
        passwordconf = self.passwordconf.get()

        #if no username or password input ask send them to the choice screen
        if len(username) == 0 or len(password) == 0:
            self.controller.show_frame(loginOrCreatePage)
            return

        if password != passwordconf:
            self.controller.show_frame(loginOrCreatePage)
            return

        #hash the recieved password
        hashObject = hashlib.sha256()
        hashObject.update(password.encode('utf-8'))
        passhash = hashObject.hexdigest()

        #
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



#Menu to display user accounts saved services and ask the user if they want to display one of the services
#information or if they want to add a new services info to be stored.
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numInput = tk.StringVar()
        self.i = 0

    #refresh the page everytime its shown
    def update(self):
        global gservicelist
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="What Would You Like To Do?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)

        #connect to the server and recieve the user accounts service info
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

        gservicelist = data
        responsearr = data.split()

        #print each of the services to the app
        i = 0
        for service in responsearr:
            if service != "S":
                tk.Label(self, text=str(i) + ". " + service).grid(row=(i+2), column=0)
            i += 1

        tk.Label(self, text=str(i) + ". " + "Add a New Password\n").grid(row=(i+2), column=0)

        tk.Label(self, text="Enter #:").grid(row=(i+3), column=0)
        tk.Entry(self, textvariable=self.numInput).grid(row=(i+4), column=0)

        self.i = i

        tk.Button(self, text="Submit", command=self.submit).grid(row=(i+5), column=0)

        tk.Button(self, text="Quit", command=self.quit).grid(row=(i+6), column=0)

    #Once the user input if they want to display a service or add a new one
    def submit(self):
        global gservice
        self.controller.show_frame(loginOrCreatePage)
        selectedOption = self.numInput.get()
        i = self.i
        self.numInput = tk.StringVar()

        #choose behavior based on user input
        if int(selectedOption) == int(i):
            self.controller.show_frame(AddServicePage)
        elif int(selectedOption) < int(i) and int(selectedOption) >= 0:
            self.controller.show_frame(DisplayServicePage)
            gservice = i
            print("Hi")
        else:
            self.controller.show_frame(MenuPage)

    def quit(self):
        self.controller.quit()




#Menu to input service information to be added for a new service to be linked with the user account
class AddServicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.service = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.key = tk.StringVar()

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.service = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.key = tk.StringVar()

        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Enter Service Information and Key").grid(row=1, column=0)
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

    #Once the user sumbits the user account info
    def addService(self):
        service = self.service.get()
        username = self.username.get()
        password = self.password.get()
        key = self.key.get()

        #if the key isnt 16 bytes or the other fileds are empty
        if len(service) == 0 or len(username) == 0 or len(password) == 0 or len(key) != 16:
            self.controller.show_frame(AddServicePage)
            return

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

        message = "AS " + service + " " + username + " " + ciphertext.hex() + " " + keyhash + " " + gusername
        client_socket.sendall(message.encode('utf-8'))

        data = client_socket.recv(1024).decode('utf-8')
        while not data:
            data = client_socket.recv(1024).decode('utf-8')
        print(f"Received response: {data}")

        client_socket.close()

        self.controller.show_frame(ContinuePage)

    def quit(self):
        self.controller.quit()




#Page to prompt the user for a
class DisplayServicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = tk.StringVar()

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.key = tk.StringVar()
        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Please Enter Key").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text="Key (16 bytes):").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.key, show="*").grid(row=4, column=0)

        tk.Button(self, text="Submit", command=self.displayService).grid(row=5, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=6, column=0)

    def displayService(self):
        key = self.key.get()

        if len(key) != 16:
            self.controller.show_frame(DisplayServicePage)
            return

        #hash the inputted key
        hashObject = hashlib.sha256()
        hashObject.update(key.encode('utf-8'))
        keyhash = hashObject.hexdigest()

        servicelist = gservicelist.split()
        service = servicelist[int(gservice) - 1]

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        message = "DS " + gusername + " " + keyhash + " " + service
        client_socket.sendall(message.encode('utf-8'))

        data = client_socket.recv(1024).decode('utf-8')
        while not data:
            data = client_socket.recv(1024).decode('utf-8')
        print(f"Received response: {data}")

        client_socket.close()

        responsearr = data.split()


        if (responsearr[0] == "Key"): #if the input key is invalid
            self.controller.show_frame(DisplayServicePage)
            return

        cipher = AES.new(key.encode(), AES.MODE_CBC, b'\x00' * AES.block_size)
        dec = cipher.decrypt(bytes.fromhex(responsearr[2]))
        pplain = Padding.unpad(dec, AES.block_size).decode()

        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Key Input Succsessful").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text=("Service: " + service)).grid(row=3, column=0)
        tk.Label(self, text=("Username: " + responsearr[1])).grid(row=4, column=0)
        tk.Label(self, text=("Password: " + pplain)).grid(row=5, column=0)

        tk.Button(self, text="Login", command=self.continuePrompt).grid(row=6, column=0)

    def continuePrompt(self):
        self.controller.show_frame(ContinuePage)

    def quit(self):
        self.controller.quit()






class ContinuePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Would You Like To Do?").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Button(self, text="Return To Menu", command=self.continueToMenu).grid(row=3, column=0)
        tk.Button(self, text="Quit", command=self.quit).grid(row=5, column=0)

    def continueToMenu(self):
        self.controller.show_frame(MenuPage)

    def quit(self):
        self.controller.quit()





class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (DisplayServicePage, ContinuePage, AddServicePage, LoginPage, CreatePage, MenuPage, loginOrCreatePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(loginOrCreatePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()





if __name__ == "__main__":
    if server_port == 0:
        floodServer()

    app = Application()
    app.geometry("300x600")
    app.mainloop()
