iptables -A FORWARD -s 10.9.0.0/24 -d 192.168.60.0/24 -p icmp --icmp-type echo-request -j DROP 
#Outside host cannot ping internal host
iptables -A INPUT -s 10.9.0.0/24 -d 10.9.0.11 -p icmp --icmp-type echo-request -j ACCEPT
iptables -A OUTPUT -d 10.9.0.0/24 -s 10.9.0.11 -p icmp --icmp-type echo-reply -j ACCEPT
#Outside host can ping the router
iptables -A FORWARD -s 192.168.60.0/24 -d 10.9.0.0/24 -p icmp --icmp-type echo-request -j ACCEPT
iptables -A FORWARD -d 192.168.60.0/24 -s 10.9.0.0/24 -p icmp --icmp-type echo-reply -j ACCEPT
#Internal hosts can ping outside hosts

iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
#All other packets between the internal and external networks should be blocked

Outside Subnet:  10.9.0.0/24
Attacker:  10.9.0.1
Outside host::  10.9.0.5

Internal Host:

192.168.60.5
192.168.60.6
192.168.60.7