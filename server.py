import socket
import sys
import os
import time
import threading


class Client:
	def __init__(self, address):
		self.address = address


class ServerSenderWorker(threading.Thread):
	def __init__(self,server_sock, file_name,name_prefix, clients):
		self.clients = clients
		self.file_name = file_name
		self.name_prefix = name_prefix
		self.sock = server_sock
		threading.Thread.__init__(self)

	def run(self):
		info = "{\"file_name\" : \"" + self.name_prefix + self.file_name + "\"}"
		content = open(self.file_name, 'rb')
		for client in self.clients:
			self.sock.sendto(bytes(info), client.address)

		for data in content:
			for client in self.clients:
				self.sock.sendto(bytes(data), client.address)
			time.sleep(0.000001)

		print('File has been sent to all clients')


class ServerConnectionWorker(threading.Thread):
	def __init__(self,clients):
		self.the_clients = clients
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		threading.Thread.__init__(self)

	def getSock(self):
		return self.sock

	def run(self):
		self.sock.bind(('127.0.0.1', 9000))

		while True:
			data, client_address = self.sock.recvfrom(1024)
			print('get request from '+str(client_address))
			if data.decode('utf-8') == 'init_connection':
				duplicate = False
				for client in self.the_clients:
					if client.address == client_address:
						duplicate = True
						break

				if not duplicate:
					self.the_clients.append(Client(client_address))
					print('New client :', client_address)

			self.sock.sendto(bytes('accepted'), client_address)


class Server(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		clients = []
		connection_worker = ServerConnectionWorker(clients)
		connection_worker.start()
		# while True:
		file_name = raw_input('Please input the file name >')
		period = input('Please input the period (seconds) >')
		counter = 0
		while True:
			ServerSenderWorker(connection_worker.getSock(), file_name, str(counter)+'-', clients).start()
			counter+=1
			time.sleep(period)


def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()