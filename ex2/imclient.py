import im
import time
import sys

server = im.IMServerProxy('http://webdev.cs.manchester.ac.uk/~mbyxalt2/IMServer.php')

if server['chatActive'].strip(' \t\n\r') == 'yes':
  userNumber = '2'
  otherUser = '1'
else:
  userNumber = '1'
  server['userTyping'] = '1'
  otherUser = '2'

server['chatActive'] = 'yes'
try:
  while server['chatActive'].strip(' \t\n\r') == 'yes':
    if server['userTyping'].strip(' \t\n\r') == userNumber:
      server['currentMessageOf' + userNumber] = ''
      server['currentMessageOf' + otherUser] = ''
      server['currentMessageOf' + userNumber] = raw_input("Type a message: ")
      server['userTyping'] = otherUser
    elif server['userTyping'].strip(' \t\n\r') == otherUser:
      while server['currentMessageOf' + otherUser].strip(' \t\n\r') == '':
        time.sleep(0.1)  
      print server['currentMessageOf' + otherUser].strip(' \t\n\r')
      server['currentMessageOf' + otherUser] == ''
except (EOFError, KeyboardInterrupt):
  print 'Exiting Chat!'
  server.clear()
  sys.exit(0)
