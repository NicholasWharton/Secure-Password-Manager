#Secure Password Manager

(CURRENT VERSION)

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

1. Ask for confirmation password when creating an account or service (also maybe confirm key when input for creating service)

2. need to add floodserver() to pmclientGUI2.py


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
