import socket
import threading
import time
import os

#server = ('45.55.207.7', 8080)
server = ('0.0.0.0', 8080)
# server = ('pi-chatter.com', 8080)

tlock = threading.Lock()
shutdown = False

def receiveThread(name, sock):
	while not shutdown:
		try:
			tlock.acquire()
			data, address = sock.recvfrom(1024)
			print str(data)
		except: pass
		finally:
			tlock.release()

host = ''
port = 0

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((host, port))
soc.setblocking(0)

receivingThread = threading.Thread(target = receiveThread, args=('oil', soc))
receivingThread.start()

try:
	os.system('clear')
except: os.system('cls')

print "###--Welcome to Peace-Pi chat server--###"
print "Type '_O' to search for online peers"
print "Type 'Quit' to exit"


class options():
	online = '2dbc2fd2358e1ea1b7a6bc08ea647b9a337ac92d'


def chatOptions(option):
	print '1. Online users'
	option = raw_input('Choose an option: ')
	if option == '1':
		return options.online
	else: 
		print 'Invalid option..'
		return False


alias = raw_input('Your Alias: ')
soc.sendto(alias, server)


while True:
	message = raw_input('')
	if message != '':
		if message.startswith('_'):
			option = chatOptions(message)
			if option: soc.sendto(option, server)
		elif message == 'Quit':
			# sure = raw_input("Are you sure?")
			soc.sendto(alias+' left', server)
			break
		else:
			soc.sendto(message, server)

	time.sleep(0.2)

shutdown = True
receivingThread.join()
soc.close()


# import hashlib
# def oH(option):
# 	passHash = hashlib.sha1()
# 	passHash.update(str(option))
# 	return passHash.hexdigest()


