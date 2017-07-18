import socket
import threading
import time
import os

#server = ('45.55.207.7', 8080)
# server = ('0.0.0.0', 8080)
server = ('localhost', 8080)
# server = ('pi-chatter.com', 8080)
loggedIn = False
tlock = threading.Lock()
shutdown = False

def receiveThread(name, sock):
	global loggedIn
	while not shutdown:
		try:
			tlock.acquire()
			data, address = sock.recvfrom(1024)
			print str(data)
			loggedIn = True
		except: pass
		finally:
			tlock.release()

host = ''
port = 0

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((host, port))
soc.setblocking(0)

receivingThread = threading.Thread(target = receiveThread, args=('oil', soc))

try:
	os.system('clear')
except: os.system('cls')

print "###--Welcome to Peace-Pi chat server--###"
print "Type '_?' for help and '_q' to quit"



class options():
	online = '2dbc2fd2358e1ea1b7a6bc08ea647b9a337ac92d'
	quit = 'f59118712ff45e3f8132cdd3ecfcfc6d3d2fa490'


def chatOptions(option=None):
	global shutdown
	if option =='_' or option =='_?':
		print "==================" 
		print 'Pi-Chatter options:\n_o\t:List online users\n_q\t:Quit\n'
		# option = raw_input('Choose an option: ')
	elif option == '_o': return options.online
	elif option == '_q':
		shutdown = True 
		return options.quit
	else: 
		print 'Invalid option. Use _? for help'
		return False


alias = raw_input('Your Alias: ')
receivingThread.start()
soc.sendto(alias, server)
print 'Connecting to server...'
startTime = time.time()
while not loggedIn and time.time()-startTime<10:
	time.sleep(1)

if not loggedIn: 
	print 'Server not reachable!'
	shutdown = True

while not shutdown:
	message = raw_input('')
	if message != '':
		if message.startswith('_'): 
			option = chatOptions(message)
			if option: soc.sendto(option, server)

		# elif message == 'Quit':
		# 	# sure = raw_input("Are you sure?")
		# 	soc.sendto(message, server)
		# 	break
		else:
			soc.sendto(message, server)

	time.sleep(0.2)


receivingThread.join()
soc.close()


# import hashlib
# def oH(option):
# 	passHash = hashlib.sha1()
# 	passHash.update(str(option))
# 	return passHash.hexdigest()


