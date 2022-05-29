from socket import *
import sys

serverName = '10.10.10.2'
serverPort = 5000
fileName = "ex.txt"

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

if len(sys.argv) == 2:
	fileName = sys.argv[1]

with open(fileName, "rb") as f:
	### Send File Contents ###
	data = f.read()
	clientSocket.send(data)

clientSocket.close()
exit()