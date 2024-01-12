#Secure Password Manager

pmclient.py: the main driver program for the client. Runs the GUI and handles the interaction between the user and the server.
  
  pmclientservices.py: holds functions that allow the adding of services to a user account and displaying this information.
  
  pmclientbuttons.py: holds the functions triggered whenever a button is pressed in the GUI

pmserver.py: is the server-side program that listens for and handles client requests. Securely receiving information from the
client or sending it. Then storing the information on the server side so it's inaccessible unless the adversary gets to the central 
system.


The password manager's security relies on the user keeping a 16-byte key confidential.
A username and password are required to login to a password manager user account. You cannot
access your service passwords without knowing the 16-byte symmetric key needed to decrypt the
password once the encrypted password is sent from the server over the socket connection. The password is 
never sent when the client authenticates itself with the password manager username and password. Instead,
the hash of the password is generated when the account is created and stored associated with the username. So
when the user logs in the username and password hash are sent to the server to be compared with the stored hash
associated with the username. This way no man in the middle can get the plain text password in transmission.


Changes made on 1/12/24:

1. made it possible for the server to handle multiple concurrent connections by creating a thread to handle each client request.

2. handled client closing connection prematurely on the server side.

3. The port number can be input through the first argument or the default value can be used on both the server and client

4. The server interface address can be added as the second argument for the client program
