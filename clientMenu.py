# Nicholas Wharton
# Secure Password Manager
# Classes for the client application to function
# 2/28/2024

import tkinter as tk
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Padding
import socket

gusername = ""
gservice = ""
gservicelist = ""

#Page to choose to login to an existing pm user account or create a new pm user account
class loginOrCreatePage(tk.Frame):
    def __init__(self, parent, controller, key, clientSocket):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = key
        self.clientSocket = clientSocket

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
        self.controller.showFrame(CreatePage)

    def loginAccount(self):
        self.controller.showFrame(LoginPage)

    def quit(self):
        self.clientSocket.close()
        self.controller.quit()




#Page to login into an existing account
class LoginPage(tk.Frame):
    def __init__(self, parent, controller, key, clientSocket):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = key
        self.clientSocket = clientSocket
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
        #pull values from the text box
        username = self.username.get()
        password = self.password.get()

        #generate password hash
        hashObject = hashlib.sha256()
        hashObject.update(password.encode('utf-8'))
        passhash = hashObject.hexdigest()

        #create the message encrypt and send to the server
        message = "L " + username + " " + passhash
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        paddedPlain = Padding.pad(message.encode(), AES.block_size)
        ciphertext = cipher.encrypt(paddedPlain)

        self.clientSocket.sendall(ciphertext)
        print("Sent Login Request to Server")

        #wait for the server to respond
        data = self.clientSocket.recv(1024)
        while not data:
            data = self.clientSocket.recv(1024)
        print("Recieved Server Response to Login Request")

        #decrypt message and switch frame based on the response
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        dec = cipher.decrypt(data)
        pplain = Padding.unpad(dec, AES.block_size).decode()

        responsearr = pplain.split()
        gusername = username

        #choose behavior based on server response
        if responsearr[1] == "Succsessful":
            self.controller.showFrame(MenuPage)
        else:
            self.controller.showFrame(loginOrCreatePage)

    def quit(self):
        self.clientSocket.close()
        self.controller.quit()





#Page used to create a new user account
class CreatePage(tk.Frame):
    def __init__(self, parent, controller, key, clientSocket):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = key
        self.clientSocket = clientSocket
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
        #get the values from the text boxes
        username = self.username.get()
        password = self.password.get()
        passwordconf = self.passwordconf.get()

        #if no username or password input ask send them to the choice screen
        if len(username) == 0 or len(password) == 0:
            self.controller.showFrame(loginOrCreatePage)
            return

        #make sure tha tthe confirm password is the same as the password input
        if password != passwordconf:
            self.controller.showFrame(loginOrCreatePage)
            return

        #hash the recieved password
        hashObject = hashlib.sha256()
        hashObject.update(password.encode('utf-8'))
        passhash = hashObject.hexdigest()

        #generate the message encrypt it and send it to the server
        message = "C " + username + " " + passhash
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        paddedPlain = Padding.pad(message.encode(), AES.block_size)
        ciphertext = cipher.encrypt(paddedPlain)

        self.clientSocket.sendall(ciphertext)
        print("Sent Create Account Request to the Server")

        #wait for the server response
        data = self.clientSocket.recv(1024)
        while not data:
            data = self.clientSocket.recv(1024)
        print("Recieved Server Response to the Create Account Request")

        #decrupt and decide what frame to switch to based on the response
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        dec = cipher.decrypt(data)
        pplain = Padding.unpad(dec, AES.block_size).decode()

        responsearr = pplain.split()
        gusername = username

        if responsearr[1] == "Succsessfully":
            self.controller.showFrame(MenuPage)
        else:
            self.controller.showFrame(loginOrCreatePage)

    def quit(self):
        self.clientSocket.close()
        self.controller.quit()



#Menu to display user accounts saved services and ask the user if they want to display one of the services
#information or if they want to add a new services info to be stored.
class MenuPage(tk.Frame):
    def __init__(self, parent, controller, key, clientSocket):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = key
        self.clientSocket = clientSocket
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

        #generate message to request the services from the server
        message = "M " + gusername
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        paddedPlain = Padding.pad(message.encode(), AES.block_size)
        ciphertext = cipher.encrypt(paddedPlain)

        self.clientSocket.sendall(ciphertext)
        print("Sending Menu Request Message")

        #wait for the servers response
        data = self.clientSocket.recv(1024)
        while not data:
            data = self.clientSocket.recv(1024)

        #decypt response to get the services related to the logged in account
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        dec = cipher.decrypt(data)
        pplain = Padding.unpad(dec, AES.block_size).decode()
        print("Received Menu Response")

        responsearr = pplain.split()

        gservicelist = pplain

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

        #self.controller.showFrame(loginOrCreatePage)
        selectedOption = self.numInput.get()
        i = self.i
        self.numInput = tk.StringVar()

        #choose behavior based on user input
        if int(selectedOption) == int(i):
            self.controller.showFrame(AddServicePage)
        elif int(selectedOption) < int(i) and int(selectedOption) >= 0:
            self.controller.showFrame(DisplayServicePage)
            gservice = i
        else:
            self.controller.showFrame(MenuPage)

    def quit(self):
        self.clientSocket.close()
        self.controller.quit()




#Menu to input service information to be added for a new service to be linked with the user account
class AddServicePage(tk.Frame):
    def __init__(self, parent, controller, key, clientSocket):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = key
        self.clientSocket = clientSocket
        self.service = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.passKey = tk.StringVar()

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.service = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.passKey = tk.StringVar()

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
        tk.Entry(self, textvariable=self.passKey, show="*").grid(row=10, column=0)

        tk.Button(self, text="Login", command=self.addService).grid(row=11, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=12, column=0)

    #Once the user sumbits the user account info
    def addService(self):
        service = self.service.get()
        username = self.username.get()
        password = self.password.get()
        passKey = self.passKey.get()

        #if the key isnt 16 bytes or the other fileds are empty
        if len(service) == 0 or len(username) == 0 or len(password) == 0 or len(passKey) != 16:
            self.controller.showFrame(MenuPage)
            return

        #get the hash of the inputted key to compare it with the saved key hash
        hashObject = hashlib.sha256()
        hashObject.update(passKey.encode('utf-8'))
        passKeyHash = hashObject.hexdigest()

        #encrypt the password with the given key
        cipher = AES.new(passKey.encode(), AES.MODE_CBC, b'\x00' * AES.block_size)
        paddedPlain = Padding.pad(password.encode(), AES.block_size)
        ciphertext = cipher.encrypt(paddedPlain)

        #Save the service name, the user name for the service, the encrypted
        #password, and a hash of the key to the users service file.
        message = "AS " + service + " " + username + " " + ciphertext.hex() + " " + passKeyHash + " " + gusername
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        paddedPlain = Padding.pad(message.encode(), AES.block_size)
        ciphertext = cipher.encrypt(paddedPlain)

        self.clientSocket.sendall(ciphertext)
        print("Sent Add Service Request to Server")

        #wait for server response
        data = self.clientSocket.recv(1024)
        while not data:
            data = self.clientSocket.recv(1024)

        print("Server Added The Service")

        #ask the user if they want to continue back to the menu or exit
        self.controller.showFrame(ContinuePage)

    def quit(self):
        self.clientSocket.close()
        self.controller.quit()




#Page to prompt the user for a
class DisplayServicePage(tk.Frame):
    def __init__(self, parent, controller, key, clientSocket):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = key
        self.clientSocket = clientSocket
        self.passKey = tk.StringVar()

    #refresh the page everytime its shown
    def update(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.passKey = tk.StringVar()
        tk.Label(self, text="-----------------------------------------").grid(row=0, column=0)
        tk.Label(self, text="Please Enter Key").grid(row=1, column=0)
        tk.Label(self, text="-----------------------------------------").grid(row=2, column=0)
        tk.Label(self, text="Key (16 bytes):").grid(row=3, column=0)
        tk.Entry(self, textvariable=self.passKey, show="*").grid(row=4, column=0)

        tk.Button(self, text="Submit", command=self.displayService).grid(row=5, column=0)
        tk.Button(self, text="Cancel", command=self.quit).grid(row=6, column=0)

    def displayService(self):
        passKey = self.passKey.get()

        if len(passKey) != 16:
            self.controller.showFrame(MenuPage)
            return

        #hash the inputted key
        hashObject = hashlib.sha256()
        hashObject.update(passKey.encode('utf-8'))
        passKeyHash = hashObject.hexdigest()

        #figure out what service the user selected to see
        servicelist = gservicelist.split()
        service = servicelist[int(gservice) - 1]

        #request the selected services stored information from the server
        message = "DS " + gusername + " " + passKeyHash + " " + service
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        paddedPlain = Padding.pad(message.encode(), AES.block_size)
        ciphertext = cipher.encrypt(paddedPlain)

        self.clientSocket.sendall(ciphertext)
        print("Sent Display Service Request to Server")

        #wait for the server response
        data = self.clientSocket.recv(1024)
        while not data:
            data = self.clientSocket.recv(1024)
        print("Recieved Display Service Response From the Server")

        #decrypt the message
        cipher = AES.new(self.key, AES.MODE_CBC, b'\x00' * AES.block_size)
        dec = cipher.decrypt(data)
        pplain = Padding.unpad(dec, AES.block_size).decode()

        responsearr = pplain.split()

        if (responsearr[0] == "Key"): #if the input key is invalid
            self.controller.showFrame(DisplayServicePage)
            return

        #decrypt the encrypted password from the decrypted message
        cipher = AES.new(passKey.encode(), AES.MODE_CBC, b'\x00' * AES.block_size)
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
        self.controller.showFrame(ContinuePage)

    def quit(self):
        self.clientSocket.close()
        self.controller.quit()






class ContinuePage(tk.Frame):
    def __init__(self, parent, controller, key, clientSocket):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key = key
        self.clientSocket = clientSocket

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
        self.controller.showFrame(MenuPage)

    def quit(self):
        self.clientSocket.close()
        self.controller.quit()
