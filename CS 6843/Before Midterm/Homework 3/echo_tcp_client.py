from socket import *
import sys

serverName = '10.10.10.2'
serverPort = 5000
message = ""

if len(sys.argv) > 1:
	for i in range(1, len(sys.argv)):
		message += str(sys.argv[i])
			message += " "

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
print("Sent: "+ str(message))
clientSocket.send(str.encode(message))
received = clientSocket.recv(1024)
print("Received: " + str(received))

clientSocket.close()