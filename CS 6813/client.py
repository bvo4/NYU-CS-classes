from socket import *
import random
import time
import sys

#serverName = '127.0.0.1'
#serverPort = 12000

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientName = "127.0.0.1"
clientSocket = socket(AF_INET, SOCK_DGRAM)


while(True):
	random_number = random.randint(0, 100)
	if(random_number < 20):
		message = 'THIS IS A REQUEST'
		clientSocket.sendto(message,(serverName, serverPort))
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		print (modifiedMessage)
	else:
		time.sleep(5)
clientSocket.close()