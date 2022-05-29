from socket import *
import random
import sys

#serverName = '127.0.0.1'
#serverPort = 12000

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientName = "127.0.0.2"
clientSocket = socket(AF_INET, SOCK_DGRAM)


while(True):
	message = 'THIS IS A REQUEST'
	clientSocket.sendto(message,(serverName, serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print (modifiedMessage)
clientSocket.close()