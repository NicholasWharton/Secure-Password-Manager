<pre>
#Secure Password Manager

(CURRENT VERSION)

clientTunnel.py: main client driver program to run the GUI and handle the interactions between the user and server.

clientMenu.py: Holds all of the application window frames to be switched between.

serverTunnel.py: main client driver program to run the handle the interactions with the user. Though this version connects to the server with a single session.

handleClients.py: holds the handle client function to process the messages recieved from the client, respond, and manage the stored data.



(FOR THE 2/29/23 ARCHIVE PROGRAM FILES)

pmclientGUI2.py: the main driver program for the client. Runs the GUI and handles the interaction between the user and the server.

pmserver.py: is the server-side program that listens for and handles client requests. Securely receiving information from the
client or sending it. Then storing the information on the server side so it's inaccessible unless the adversary gets to the central
system.



(FOR THE 1/13/23 ARCHIVE PROGRAM FILES)

pmclient.py: the main driver program for the client. Runs the GUI and handles the interaction between the user and the server.

  pmclientservices.py: holds functions that allow the adding of services to a user account and displaying this information.

  pmclientbuttons.py: holds the functions triggered whenever a button is pressed in the GUI

pmserver.py: is the server-side program that listens for and handles client requests. Securely receiving information from the
client or sending it. Then storing the information on the server side so it's inaccessible unless the adversary gets to the central
system.




(SECURITY)

This version connects the server and client with a single session where all messages are encrypted. This encryption is handled by sharing a symmetric key using RSA public key encryption at the start of each session.

Now each message that is sent is completly encrypted using AES CBC-mode using the symmetric key shared.

The password manager's security relies on the user keeping a 16-byte key confidential.
A username and password are required to login to a password manager user account. You cannot
access your service passwords without knowing the 16-byte symmetric key needed to decrypt the
password once the encrypted password is sent from the server over the socket connection. The password is
never sent when the client authenticates itself with the password manager username and password. Instead,
the hash of the password is generated when the account is created and stored associated with the username. So
when the user logs in the username and password hash are sent to the server to be compared with the stored hash
associated with the username. This way no man in the middle can get the plain text password in transmission.

The program uses SHA256 Hashes and AES CBC encryption with 128 bit keys



Future Changes to Make:

1. Add signatures to provide accountability to messages.

2. Add salting to the encryption workflow for passwords before sent and stored.

3. Create a way to identify the user based on the system that they create the account on so you can only access the account if you are useing the physical device that the account was created with.

4. Make the menu response for the server to request the user name and password rather than just the username. Since anyone who gets the session key could just request any users menu information.



Changes made on 2/29/24:

1. All menus in the client menu now interact with the server using AES CBC-mode encrypted messages.

2. Commented The code to better the readability\

3. Set the tunneled program as the current version and archvied the GUI2 version



Changes made on 2/28/24:

1. Completed the symmetric key establishment process.

2. Converted the functionality of the upgraded GUI client application and the servers client handler function to work in a single session.

3. Set up all messaging to be AES CBC encypted, though it isnt working.



Changes made on 2/27/24:

1. Started working on the clientTunnel.py and serverTunnel.py version of the program to use a single session rather than reestablishing the socket connection for every message. Then a symmetric session key can be generated to encrypt all messages being sent between the client and server.

Changes made on 1/16/24:

1. Fixed Display Service page to deal with the invalid key input that is 16 bytes. Also fixed the text boxes to reset upon update.

2. Centered the elements on the page horizontally

3. Added floodserver() functionality to pmclientGUI2.py

4. Added confirmation password when creating an account or service


Changes made on 1/15/24:

1. Added page that prompt user if they want to continue to menu or quitting after adding a new service.

2. Fixed the updating of pages so they are cleared before they update. While also making it so the page is updated when its switch too rather than just on initialization.

3. Added the displayService() function to pmclientGUI2.py which is now fixed to only compares the generated key hash with the record associated with the choosen service in the menu.


Changes made on 1/14/24:

1. new client program created named pmclientGUI2.py which completly changes the way that the GUI functions. Instead of deleting the window after every operation. Pages are now constructed and switched between on a single window making the experience more seamless.

2. Added (and reworked) the functionality to pmclientGUI2.py to create user accounts, login to user accounts, interact with the account menu, and add new services. While still maintaining the same functionality with the server which had been established when building the original version of the program.

Changes made on 1/13/24:

1. added floodServer() function to client program so if the server is  listening on a port within the range 1024-60000. The client will flood these ports with attempting to transmit a discover message and waits until it connects to and gets the appropriate response from the server.


Changes made on 1/12/24:

1. made it possible for the server to handle multiple concurrent connections by creating a thread to handle each client request.

2. handled client closing connection prematurely on the server side.

3. The port number can be input through the first argument or the default value can be used on both the server and client

4. The server interface address can be added as the second argument for the client program

</pre>
