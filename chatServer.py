#!usr/bin/ent python

import socket
import time
from random import choice

HOST = '0.0.0.0'
PORT = 8080


class Client():

	def __init__(self, alias, address):
		self.alias = alias
		self.aliasC = self.colorize(self.alias)
		self.address = address

	def randomColor(self):
		return choice(['0;31','1;31','0;32','1;32','0;33','1;33','0;34','1;34','0;35m','1;35m','0;36','1;36','0;37','1;37'])

	def colorize(self, message):
		return "\033[{}m".format(self.randomColor())+message+"\033[0m"



class options():
	online = '2dbc2fd2358e1ea1b7a6bc08ea647b9a337ac92d'
	quit = 'f59118712ff45e3f8132cdd3ecfcfc6d3d2fa490'



class chatRoom():
	socket = ""

	def __init__(self, host, port):
		self.socket = self._udpSocket(host, port)
		self.members = {}
		self.memberCount = 0

	@staticmethod
	def _udpSocket(host, port):
		try:
			socc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#UDP socket
			socc.bind((host, port))
			# soc.setblocking(0)
			print "Server started", "("+str(host)+":"+str(port)+")"
			return socc
		except Exception, e:
			print 'Server failed to initiate:', e

	def addMember(self, alias, address):
		self.members[address] = Client(alias, address)
		self.memberCount += 1
		return self.members[address]

	def member(self, address):
		if self.contains(address):
			return self.members[address]
		else:
			return False

	def removeMember(self, member):
		if self.contains(member.address):
			del self.members[address]
		else:
			print "Member not found"

	def getAllMembers(self):
		return [value for key, value in self.members.iteritems()]

	def contains(self, address):
		for add, value in self.members.iteritems():
			if add == address: return True
		return False

	def colorize(self, message):
		return "\033[38;5;117m"+message+"\033[0m"
		# return "\033[5;1;37m"+message+"\033[0m" 			#Blinking!

	def send(self, message, member):
		self.socket.sendto(message, member.address)    # sendto() is for UDP. send() is for TCP

	def sendAll(self, message, sender = None):
		for mem in self.getAllMembers():
			if mem.address != sender.address:
				self.send(message, mem)

	@staticmethod
	def log(message, member):
		chatLog = "./chatLog.log"
		with open(chatLog, "a") as logger:
			logger.write(str(member.address) + time.ctime(time.time()) + ':' + str(message)+'\n')

	def close(self):
		self.socket.close()


#-------Run time functions------------------

def checkOption(data, member):
	if len(data) == 40:
		if data == options.online:
			message=""
			for m in room.getAllMembers():
				if message == "": message+=m.aliasC
				else: message+=", "+m.aliasC
			room.send(message, member)

		elif data == options.quit: 
			message = room.colorize("{} left Pi-Chatter".format(member.alias))
			room.sendAll(message, sender=member)
			room.removeMember(member)
		else: return False
		room.log(message, member)
		return True
	else: return False 


if __name__ == '__main__':

	room = chatRoom(HOST, PORT)
	quitting = False

	while not quitting:
		try:
			data, address = room.socket.recvfrom(1024)        	#recvfrom() is for UDP. recv() is for TCP

			if not room.contains(address):
				member = room.addMember(data, address)
				room.send(room.colorize("You are online on Pi-Chatter!"), member)
				message = member.aliasC+room.colorize(' is online')
				room.sendAll(message, sender=member)
				room.log(message, member)
			else:
				member = room.member(address)
				option = checkOption(str(data), member)
				if not option:
					message = member.aliasC + room.colorize(' -> ') + str(data)
					room.sendAll(message, sender=member)
					room.log(message, member)
				# else: 
					
			
		except Exception, e:
			print 'Error=',e
			quitting = True

	room.close()






