import sys
from ex3utils import Server

numberOfUsers = 0
usersOnServer = {}
privateChats = {}

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
            print "User has requested " + parameter + " as a username."
            global usersOnServer
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
                                                        }
            print "------------------------------"

        if command == 'SENDALL':
            print "---------- SENDALL ----------"
            print "User " + socket.screenName + " has sent a message to all users."
            for username in usersOnServer:
                socketOfUser = usersOnServer[username]['socket']
                if socket.screenName != username:
                    socketOfUser.send(socket.screenName + ": " + parameter)
                else:
                    socketOfUser.send("you: " + parameter)
            print "-----------------------------"
        return True

        if command == 'SEND':
            print "---------- SEND ----------"
            (username, newparamter) = parameter.strip().partition(' ')
            if username in usersOnServer:
                print socket.screenName + " sent message to " + newparamter + "."
                socketOfUser = usersOnServer[username]['socket']
                socketOfUser.send(socket.screenName + ": " + parameter)
            else:
                print socket.screenName + " sent message to user that doesn't exsist."
                socket.send("There is no such user!")
            print "------------------------------"

    def onDisconnect(self, socket):
        print socket.screenName + " has disconnected from the server."
        del usersOnServer[socket.screenName]
        global numberOfUsers
        numberOfUsers -= 1
        print "There are " + str(numberOfUsers) + " users connected"

    def onStop(self):
        print "The server has stopped"

ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()

server.start(ip,port)
