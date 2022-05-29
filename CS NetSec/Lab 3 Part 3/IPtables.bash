#All the internal hosts run a telnet server (port 23)
iptables -A FORWARD -s 10.9.0.0/24 -d 192.168.60.5 -i eth0 -o eth1 -p tcp --dport 23 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -d 10.9.0.0/24 -s 192.168.60.5 -i eth1 -o eth0 -p tcp --sport 23 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

#Outside hosts cannot access other internal servers.
iptables -A FORWARD -s 10.9.0.0/24 -d 192.168.60.0/24 -i eth1 -o eth0 -p tcp --dport 23 -m conntrack --ctstate NEW -j DROP

#Internal hosts can access all the internal servers
iptables -A FORWARD -s 192.168.60.0/24 -d 192.168.60.0/24 -i eth1 -o eth1 -p tcp --sport 23 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
iptables -A FORWARD -s 192.168.60.0/24 -d 192.168.60.0/24 -i eth1 -o eth1 -p tcp --dport 23 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT

#Add a rule allowing internal hosts to visit any external server
iptables -A FORWARD -d 10.9.0.0/24 -s 192.168.60.0/24 -i eth1 -o eth0 -p tcp --dport 23 -m conntrack --ctstate NEW -j ACCEPT
iptables -A FORWARD -d 10.9.0.0/24 -s 192.168.60.0/24 -i eth1 -o eth0 -p tcp --dport 23 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -s 10.9.0.0/24 -d 192.168.60.0/24 -i eth0 -o eth1 -p tcp --sport 23 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT


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

