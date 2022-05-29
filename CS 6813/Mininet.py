from mininet.topo import Topo
from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
import time

#sudo mn -c
#has to be run on mininet everytime the script is executed to clear files
# To run:  python2.7 Mininet.py

"""
This class is responsible for creating the custom network topology in the format.
				Core (c1)
				Aggregation Layer (a1, a2,... aN)
				Edge Layer (e1, e2, ... eN)
				Host Layer (h1, h2, h3,... hN)
Only the host layer will hold the actual hosts.  The layers above will contain switches and links to direct to each host
"""

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )


topos = { 'mytopo': ( lambda: MyTopo() ) }

class DataCenterTopo(Topo):
    "Data-center topology with variable number of hosts spread evenly across all edge nodes."
    def __init__(self, count, **opts):
        Topo.__init__(self)

        """
----------------------------------------------------------CORE LAYER------------------------------------------------
        """
        #Create switch
        core = self.addSwitch('c1')
        print ("Core Switch added, moving onto Aggregation layer")


        bw = 10 #Link bandwidth
        delay = '5ms'
        loss = 5
        max_queue_size = 1000

        #Network layers
        aggregation = [] * 0
        edges = [] * 0
        hosts = [] * 0
        """
----------------------------------------------------------AGGREGATION LAYER--------------------------------------------
        """

        for aCount in range(1, 3):
            switch = self.addSwitch('a' + str(aCount)) #Adds a switch to the topology and provides the switch name

            #Connect host with a switch by creating a link between the switch and host
            self.addLink(core, switch, bw=bw, delay=delay, loss=loss, max_queue_size=max_queue_size, use_htb=True)
            aggregation.append(switch)
            print ('Aggregation switch number ' + str(aCount) + " added")

        """
----------------------------------------------------------EDGE LAYER--------------------------------------------
        """
        
        #Recording switches added in edge layer
        SwitchCount = 1

        for aggregationswitch in aggregation:
            for i in range(1, 3):
                edgeswitch = self.addSwitch('e' + str(SwitchCount))  #Adds a switch to the edge of the topology
                self.addLink(aggregationswitch, edgeswitch, bw=bw, delay=delay, loss=loss, max_queue_size=max_queue_size, use_htb=True) #Adds a bidirectional link to the topology
                print ("Edge Number " + str(edgeswitch) + " added")
                edges.append(edgeswitch)
                SwitchCount += 1


        """
----------------------------------------------------------Host LAYER--------------------------------------------
	"""
        
	HostCount=1
	count = 32
	print("HOST NUMBER:  " + str(HostCount))
	print("COUNT: " + str(count))
	
        while (HostCount < count):
            for edge in edges:
                if HostCount > count:
                    break
                #Adds host to topology
                host = self.addHost('h' + str(HostCount), cpu=.5/count)
                #Creates a bidirectional link between an edge and the host
                self.addLink(edge, host)
                hosts.append(host)
                #print("Host number " + str(host) + " added")
                HostCount += 1
	
	print("HOSTS" + str(hosts))
	
def DDosScript():

	for clients in range(3, 6):
		HostCount = 2 ** clients

	print("We have " + str(HostCount) + " number of hosts")
	"""
	-----------------------------Setup Time-----------------------------
	"""
	setupTime = time.time()

	#Create the data center topology
	topology = DataCenterTopo(HostCount)
	net = Mininet(topo=topology, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
	#Starts the network
	net.start()

	#Create topology host
	host = net[ 'h1' ]
	#Port number can be extracted from host but unclear if port number can be extracted
	port = 80

	host.sendCmd('python server.py')

	#Recording time for logging purposes
	setupTime = setupTime - time.time()
	print ("Setup took " + str(setupTime) + " seconds")
	print("Sending to " + str(host.IP() + ":" + str(port)))

	"""
	-----------------------------DDoSING TIME-----------------------------
	"""

	hackingTime = time.time()
	import re
	for node in net:
		if not re.match("(h1|c|a|e)", node):
			host = net[node]
			host.sendCmd('python2.7 attacker.py %s' % str(host.IP()) + " " + str(port))
			#host.sendCmd('python2.7 client.py %s')
			
		print ("Initiating for 30 seconds")
		time.sleep(30)

		#Record time for later purposes
		hackingTime = time.time() - hackingTime
		print ("Testing took %d seconds" % hackingTime)

	"""	
	-----------------------------Closing Time-----------------------------
	"""

	EraseTime = time.time()
	net.stop() #Stops network
	host.sendCmd('sudo mn -c') #Remove the links from file
	ErasedTime = time() - EraseTime

	"""	
	-----------------------------Results-----------------------------
	"""

	print ("Cleanup took %d seconds" % str(ErasedTime))
	print ("Done")

if __name__ == '__main__':
	startingTime = time.time()
	#setLogLevel('output')
	DDosScript()
	startingTime = startingTime - time.time()