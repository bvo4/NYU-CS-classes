from socket import *
import sys
import os

serverPort = 5000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.list(5)
fileName = "serverOutput.txt"

while 1:
	connectionSocket, address = serverSocket.accept()
	fileWrite = open(fileName, 'wb')
	file = connectionSocket.recv(1024)
#	Name = False
	
	with fileWrite as f:
		### Extract the Name of the file ###
		### The file name is provided by the client ###
		#if not Name:
		#	newName = file.decode().partition('\n')[0]
		#	print("Changing name to " + newNam)
		#	os.rename(fileName, newName)
			#Pop the first line because the client was set up to send the name of the text file as the first line
		#	file = file.decode().split(\n', 1)[-1]
		### Rename the file to the intended name received from the client ###
		
		if not file:
			print("File could not be opened")
			break
			
			fileWrite.write(file)
		fileWrite.close()
		break

connectionSocket.close()
exit()