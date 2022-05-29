import socket
import dns.resolver
import binascii
import re

#To Do:  Add flexibility.  Allow input for any website for an A record.
#Make it flexibly identify and grab the IP Address from teh Answer Layer.

def STRIP_RESPONSE(Final_Message):

    #-1 means 0001 not found.  This means there's no sign of an A record here.
    if(Final_Message.find('0001') == -1):
        print("ERROR:  A RECORD NOT FOUND")
        return

    #print("STRIP RESPONSE:  " + Final_Message)
    
    #Strip the pointer
    #pointer = Final_Message[0:1]
    #Final_Message = Final_Message[1:]
    #print("POINTER: " + pointer)
    
    #Strip the offset
    #offset = Final_Message[0:3]
    #Final_Message = Final_Message[3:]
    #print("offset: " + offset)
    
    
    #Search for the A RECORD query
    while(Final_Message):
        
        record = Final_Message[0:4]
        Final_Message = Final_Message [4:]
        if record != '0001':
            #This is not an A record.  Strip out the rest of the record response and start on the next DNS record message
            #print ("ERROR:  THIS IS NOT AN A RECORD :  " + record)
            Final_Message = Final_Message [4:]  #Skip the Class type
            i = Final_Message.find('0001')      #Find the A RECORD
            Final_Message = Final_Message[i:]   #Skip to the A RECORD
        else:
            #print("record: " + record)
            break
    
    #Strip the class type
    classType = Final_Message[0:4]
    Final_Message = Final_Message[4:]
    #print("classType: " + classType)
    
    #STRIP THE TIME RESPONSE
    TIMEOUT = Final_Message[0:8]
    Final_Message = Final_Message[8:]
    #print("timeout: " + TIMEOUT)
    
    #STRIP THE ADDRESS SIZE
    ADDRESS_SIZE = Final_Message[0:4]
    Final_Message = Final_Message[4:]
    #print("ADDRESS_SIZE: " + ADDRESS_SIZE)
    
    #FOUND THE IP ADDRESS
    #Will depend on ADDRESS_SIZE in BYTES AS WELL
    try:    IP = Final_Message[0:2*int(ADDRESS_SIZE)]
    except Exception as e:
        #print("EXCEPTION")
        IP = STRIP_RESPONSE(Final_Message)
    return IP

def DNSREQUEST(value, DNS):
        
    ###############################################Header layer###################################################
    ID="db42"               #Response should have the same ID
    QR="01 00 00 01"         #QR, OPCODE, AA, TC, RD
    HEAD = "00 00 00 00"     #RA, Z, RCODE, QDCOUNT, ANCOUNT
    QDCOUNT="00 00"          #NSCOUNT, ARCOUNT = 0
    
    HEADERLAYER = ID + QR + HEAD + QDCOUNT
    HEADERLAYER = HEADERLAYER.replace(" ", "").replace("\n", "")    #Strip the extra space and end line notation
    
    ###############################################Question layer###################################################
    QLayer = ''
    
    WEBSITE = value.split(".")      #Take the IP Address from the input and convert it into ASCII
    for i in range(len(WEBSITE)):
        Temp = binascii.hexlify(WEBSITE[i].encode()).decode("UTF-8")
        length  = str(int(len(Temp)/2))
        length = length.zfill(2)
        QLayer += length + Temp

    #print("QLAYER: " + QLayer)
    QLayer = QLayer.replace(" ", "").replace("\n", "")

    ###############################################Answer layer###################################################
    ENDOF = "00"
    NAME="00 01"          #A RECORD QUERY
    TYPE="00 01 00 01"    #IN RECORD
    CLASS="01"            #Internet Address
    
    ANSWERLAYER = ENDOF + NAME + TYPE + CLASS
    ANSWERLAYER = ANSWERLAYER.replace(" ", "").replace("\n", "")
    
    message = HEADERLAYER + QLayer + ANSWERLAYER
    
    ##############################################SENDING DNS A RECORD REQUEST####################################
    
    message = message.replace(" ", "").replace("\n", "")        #Must remove the \n from the string
    #print("Sending:  \t\t" + message)
    
    server_address = (DNS, 53)                                   #Send to 8.8.8.8, port 53
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #Send on a UDP socket
    sock.settimeout(5.0)                                        #If we can't connect within X Seconds, it must not be a valid address.
    
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
        
    except Exception as e:
        print("ERROR:  DESTINATION NOT AVAILABLE")
        print ("REASON:  ", e)
        return
        
    finally:
        sock.close()
        
    #The last few bits of the ASCII code will contain the IP Address
    Final_Message = binascii.hexlify(data).decode("utf-8")

    #print("RESPONSE MESSAGE:  \t" + Final_Message)
    IP_ADDRESS = Final_Message[-8:]
    
    if (len(Final_Message) <= len(message)):
        print("ERROR:  THIS DOESN'T APPEAR TO BE A VALID IP ADDRESS")
        print("HEX CODE:  " + IP_ADDRESS)
        return
        
        
    ##################################STRIP LAYER###########################################################
    #Strip out the ID Header
    RESPONSE = Final_Message[0:len(HEADERLAYER)]
    Final_Message = Final_Message[len(HEADERLAYER):]
    #print("HEADER LAYER: " + RESPONSE)
    
    #Strip out the Domain Name & the end of domain name 00
    DOMAIN = Final_Message[:len(QLayer) + 2]
    Final_Message = Final_Message[len(QLayer) + 2:]
    #print("DOMAIN:  " + DOMAIN)
    
    #STRIP OUT THE QUERIES
    counter = 0
    QUERY = ''
    #STRIP THE QDCOUNT, ARCOUNT, NSCOUNT, AND ARCOUNT respectively
    while (counter < 4):
        QUERY += Final_Message[0:2]
        Final_Message = Final_Message[2:]
        counter = counter + 1
    #print("QUERY: " + QUERY)
    
    #The rest of the message after this point will be added by the DNS Server

    #Strip out all parts until we get the resulting message with the IP ADDRESS
    IP_ADDRESS = STRIP_RESPONSE(Final_Message)
 
    ##########################################STRIP LAYER########################################################
    
    #Answer_Header = Final_Message[:-8]   #Holds the Type, CLass, TTL, RDLength, and RDATA
    #Final_Message = Final_Message[-8:]   #Strip off the Answer header of the packet
    print("HEX CODE:  " + IP_ADDRESS[:2] + " " + IP_ADDRESS[2:4] + " " + IP_ADDRESS[4:6] + " " + IP_ADDRESS[6:8])
    
    #Get the sequence of numbers associated with the IP Address

    Primary = int(IP_ADDRESS[0:2], 16)
    Secondary = int(IP_ADDRESS[2:4], 16)
    Tertiary = int(IP_ADDRESS[4:6], 16)
    Quatiary = int(IP_ADDRESS[6:8], 16)


    DNS_ADDRESS = str(Primary) + "." + str(Secondary) + "." + str(Tertiary) + "." + str(Quatiary)
    print("DNS_ADDRESS FOUND AT : " + DNS_ADDRESS)

if __name__ == '__main__':
    value = input("Input the website's domain name:  ")
    value = value.replace(" ", "").replace("\n", "")
    
    DNS = input("Input the IP Address of the DNS server to contact:  ")
    DNS = DNS.replace(" ", "").replace("\n", "")
    
    DNSREQUEST(value, DNS)