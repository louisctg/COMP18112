import sys
from ex3utils import Server

numberOfUsers = 0

class MyServer(Server):

    def onStart(self):
        global numberOfUsers
        print "The server has started"

    def onConnect(self, socket):
        print "A client has connected"
        global numberOfUsers
        numberOfUsers += 1
        print "There are " + str(numberOfUsers) + " users connected"

    def onMessage(self, socket, message):
        print "A message has been recived"

    def onDisconnect(self, socket):
        print "A client has disconnected"
        global numberOfUsers
        numberOfUsers -= 1
        print "There are " + str(numberOfUsers) + " users connected"

    def onStop(self):
        print "The server has stopped"

ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()

server.start(ip,port)
server.stop()
