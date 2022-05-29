from socket import *
import sys
import random
import time

def stall(max):
	random_number = random.randint(0, max)
	return random_number
class address:
	def __init__(self):
		self.IP = 0
		self.LRU = 0

	def __init__(self, IP, LRU):
		self.IP = IP
		self.LRU = LRU

serverName = "10.0.0.1"
serverPort = 80

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverAddress = (serverName, serverPort)
serverSocket.bind(serverAddress)

print ("The server is ready to receive")

buffer_list = [None] * 300
buffer_size = 0

IP_ADDRESS_LIST = [None]* 5
IP_ADDRESS_SIZE = 0

Found = False
Service = True

while (True):	
	message, clientAddress = serverSocket.recvfrom(2048)
	print("IP ADDRESS: " + str(clientAddress[0]))

	if(buffer_size < 300):
		buffer_list[buffer_size] = message
		buffer_size = buffer_size + 1
		IP_ADDRESS_LIST[IP_ADDRESS_SIZE % 5] = address(clientAddress[0], 0)
		IP_ADDRESS_SIZE = IP_ADDRESS_SIZE + 1
	
	else:
		for IP_ADDRESS in range(0, len(IP_ADDRESS_LIST)):
			if(clientAddress[0] == IP_ADDRESS_LIST[IP_ADDRESS].IP):
				IP_ADDRESS_LIST[IP_ADDRESS].LRU = 0
				Found = True
				break
			else:
				IP_ADDRESS_LIST[IP_ADDRESS].LRU = IP_ADDRESS_LIST[IP_ADDRESS].LRU + 1
		
		if(Found == False):
			maximum = 0;
			pivot = 0
			counter = 0
			
			for IP_ADDRESS in IP_ADDRESS_LIST:
				if(maximum > IP_ADDRESS_LIST[IP_ADDRESS].LRU):
					maximum = IP_ADDRESS_LIST[IP_ADDRESS].LRU
					pivot = IP_ADDRESS
					counter = counter + maximum
			
			if(counter > 5):
				IP_ADDRESS_LIST[pivot].IP = clientAddress[0]
				IP_ADDRESS_LIST[pivot].LRU = 0
				Service = False
			else:
				Service = True
				break
		Found = False
		buffer_list[buffer_size%300] = message
	
	#service = True
	if(Service == True):
		random_number = stall(10000)
		modifiedMessage = str(random_number)
		serverSocket.sendto(modifiedMessage, clientAddress)
		
		