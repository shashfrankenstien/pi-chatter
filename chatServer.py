#!usr/bin/ent python

import socket
import time

HOST = '0.0.0.0'
PORT = 8080


class Client():
	def __init__(self, alias, address):
		self.alias = alias
		self.address = address

# class Message():
# 	_count = 0
# 	def __init__(self, mess):
# 		self.message, self.sender = mess
# 		_count += 1

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
		return Client(alias, address)

	def member(self, address):
		if self.contains(address):
			return self.members[address]
		else:
			return False

	def removeMember(self, address):
		if self.contains(address):
			del self.members[address]
		else:
			print "Member not found"

	def getAllMembers(self):
		return [value for key, value in self.members.iteritems()]

	def contains(self, address):
		for add, value in self.members.iteritems():
			if add == address: return True
		return False

	def send(self, message, member):
		self.socket.sendto(message, member.address)    # sendto() is for UDP. send() is for TCP


	def sendAll(self, message, leaveout = None):
		for mem in self.getAllMembers():
			if mem.address != member.address:
				self.send(message, mem)

	@staticmethod
	def log(message, member):
		print str(member.address) + time.ctime(time.time()) + ':' + str(message)

	def close(self):
		self.socket.close()


def checkOption(data, member):
	global options
	if len(data) == 40:
		if data == options.online:
			message = [m.alias for m in room.getAllMembers()]
			room.send(str(message), member)
		elif data == options.quit: 
			message = "{} left pi-chatter".format(member.alias)
			room.sendAll(message, leaveout=member)
			room.removeMember(member.address)
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
				room.send("You are online on Pi-Chatter!", member)
				message = member.alias+' is online'
				room.sendAll(message, leaveout=member)
				room.log(message, member)
			else:
				member = room.member(address)
				option = checkOption(str(data), member)
				if not option:
					message = member.alias + ' -> ' + str(data)
					room.sendAll(message, leaveout=member)
					room.log(message, member)
				# else: 
					
			
		except Exception, e:
			print 'Error=',e
			quitting = True

	room.close()






