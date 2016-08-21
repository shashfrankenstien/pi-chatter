import socket
import threading
import time
import os

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

# server = ('192.168.0.25', 5000)
server = ('0.0.0.0', 8080)
# server = ('pi-chatter.com', 8080)

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((host, port))
soc.setblocking(0)

receivingThread = threading.Thread(target = receiveThread, args=('oil', soc))
receivingThread.start()

try:
	os.system('clear')
except: os.system('cls')

print "###--Welcome to Peace-Pi chat server--###"
# print "Type '_OnLine' to search for online peers"
print "Type 'Quit' to exit"



def chatOptions(option):
	global soc, server
	if option == '_Online':
		soc.sendto("!@#checkonline", server)
	else: print 'Invalid option..'


alias = raw_input('Your Alias: ')
soc.sendto(alias, server)
# print 'You are online!'
# # message = ''

while True:
	message = raw_input('')
	if message != '':
		if message.startswith('_'):
			chatOptions(message)
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


