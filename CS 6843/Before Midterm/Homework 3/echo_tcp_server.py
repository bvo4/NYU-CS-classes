from socket import *

serverPort = 5000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while 1:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)
	print("Received: " + sentence.decode())
	
	if(sentence.decode().find('SECRET') >= 0):
		digits = 0
		digit_string = ""
		
		for x in sentence.decode():
			if x.isdigit():
					digits = digits + 1
					digit_string = digit_string + str(x)
					
			connectionSocket.send(("Digits: " + digit_string + " Count: " + str(digits) + ".").encode())
	else:
		connectionSocket.send(("Secret code not found.\n".encode())
	
	connectionSocket.close()