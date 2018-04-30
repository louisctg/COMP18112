"""

IRC client exemplar.

"""

import time,readline,thread
import sys,struct,fcntl,termios
from ex3utils import Client

import time

screenName = '';
class IRCClient(Client):


	def onMessage(self, socket, message):
		# *** process incoming messages here ***
		if not message.startswith('you'):
			(rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))

			text_len = len(readline.get_line_buffer()) + 2 		# Room for line buffe and '> '

			# ANSI escape sequences (All VT100 except ESC[0G)
			sys.stdout.write('\x1b[2K')                         # <ESC> Delete current line
			sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))  # <ESC> Move cursor up
																# <ESC> Delete current line
			sys.stdout.write('\x1b[0G')                         # <ESC. Move to start of line
			print message
			sys.stdout.write('> ' + readline.get_line_buffer())
			sys.stdout.flush()
		else:

			# ANSI escape sequences (All VT100 except ESC[0G)
			sys.stdout.write('\x1b[2K')                         # <ESC> Delete current line
			sys.stdout.write('\x1b[1A\x1b[2K')  				# <ESC> Move cursor up
																# <ESC> Delete current line
			sys.stdout.write('\x1b[0G')                         # <ESC. Move to start of line
			sys.stdout.flush()
			message.replace(screenName, "you", 1)
			print message;
		return True


# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])
screenName = sys.argv[3]

# Create an IRC client.
client = IRCClient()

# Start server
client.start(ip, port)

# *** register your client here, e.g. ***
client.send('REGISTER %s' % screenName)

while client.isRunning():
	try:
		sys.stdout.write('\x1b[0G')                         # <ESC. Move to start of line
		command = raw_input("> ").strip()
		client.send(command)
		# *** process input from the user in a loop here ***
		# *** use client.send(someMessage) to send messages to the server
	except:
		client.stop();

client.stop()
