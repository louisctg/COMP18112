import sys, getpass
from ex3utils import Server

numberOfUsers = 0
usersOnServer = {}
groups = []
adminpass = ''
class MyServer(Server):

    def onStart(self):
        global numberOfUsers
        print "The server has started"

    def onConnect(self, socket):
        print "A client has connected"
        socket.screenName = None

        ##Increment active users and print the total number
        global numberOfUsers
        numberOfUsers += 1
        print "There are " + str(numberOfUsers) + " users connected"

    def onMessage(self, socket, message):
        (command, sep, parameter) = message.strip().partition(' ')
        if command == 'REGISTER':
            print "---------- REGISTER ----------"
            """ Register's user on network """
            print "User has requested " + parameter + " as a username."
            global usersOnServer

            # CHeck if the user is on the server
            if parameter in usersOnServer:
                print "Username already in use. Disconnecting user."
                socket.send("This user already exists!")
                return False
            else:
                print "Username is allowwed."
                socket.screenName = parameter

                #Add user to connected users
                print "Adding user to server."
                usersOnServer[parameter] = {
                                            "allowed": 'yes',
                                            "socket": socket,
                                            "type": 'user',
                                                        }

            print "------------------------------"
        elif command == 'SENDALL':
            print "---------- SENDALL ----------"
            if usersOnServer[socket.screenName]['allowed'] == 'yes':
                """ Sends message to all users """
                print "User " + socket.screenName + " has sent a message to all users."

                # Send message to all users including sender (but start with 'you: ')
                for username in usersOnServer:
                    socketOfUser = usersOnServer[username]['socket']
                    if socket.screenName != username:
                        socketOfUser.send(socket.screenName + ": " + parameter)
                    else:
                        socketOfUser.send("you: " + parameter)
            else:
                socket.send("You are banned from sending messages!")
            print "-----------------------------"
        elif command == 'SEND':
            print "---------- SEND ----------"
            """ Sends message to specific user """
            if usersOnServer[socket.screenName]['allowed'] == 'yes':
                (username, sep, newparameter) = parameter.strip().partition(' ')
                if username in usersOnServer:
                    print socket.screenName + " sent message to " + username + "."
                    socketOfUser = usersOnServer[username]['socket']
                    socketOfUser.send(socket.screenName + " PRIVATE to you: " + newparameter)
                    socket.send("you PRIVATE to " + socketOfUser.screenName + ": " + newparameter)
                else:
                    print socket.screenName + " sent message to user that doesn't exsist."
                    socket.send("There is no such user!")
            else:
                socket.send("You are banned from sending messages!")
            print "------------------------------"
        elif command == 'ADMIN':
            """ Enables admin privileges for the user """
            if usersOnServer[socket.screenName]['type'] != 'admin':
                global adminpass
                if parameter == adminpass:
                    usersOnServer[socket.screenName]['type'] = 'admin'
                else:
                    socket.send("You have been denied admin privileges!")
            else:
                socket.send("You are already and admin!")
        elif command == 'ADCMD':
            if usersOnServer[socket.screenName]['type'] == 'admin':
                (admincommand, sep, newparameter) = parameter.strip().partition(' ')
                if admincommand == 'BAN':
                    if newparameter in usersOnServer:
                        usersOnServer[newparameter]['allowed'] = 'no'
                    else:
                        socket.send("The user is not on the server!")
                elif admincommand == 'ALLOW':
                    if newparameter in usersOnServer:
                        usersOnServer[newparameter]['allowed'] = 'yes'
                    else:
                        socket.send("The user is not on the server!")
                elif admincommand == 'WHO':
                    socket.send("Users Connected:")
                    for user in usersOnServer:
                        socket.send(user)
                elif admincommand == 'NEWPASS':
                    adminpass = newparameter
                elif admincommand == 'PRINTPASS':
                    socket.send("Password is: '" + adminpass + "'")
                else:
                    socket.send("The admin command wasn't found!")
            else:
                socket.send("You do not have admin privileges!")
        else:
            socket.send("There is no such command: " + command)

        return True

    def onDisconnect(self, socket):
        if socket.screenName == None:
            print "User has been disconnected without registering."
        else:
            print socket.screenName + " has disconnected from the server."
            del usersOnServer[socket.screenName]
        global numberOfUsers
        numberOfUsers -= 1
        print "There are " + str(numberOfUsers) + " users connected"

    def onStop(self):
        print "The server has stopped"

ip = sys.argv[1]
port = int(sys.argv[2])
adminpass = getpass.getpass("Enter password: ")


server = MyServer()

server.start(ip,port)
