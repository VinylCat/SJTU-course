from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from sys import argv

class SingleSwitchTopo(Topo):
    def build(self):
        switch1 = self.addSwitch('s1', stp = True)
        switch2 = self.addSwitch('s2',stp=True)
        switch3 = self.addSwitch('s3',stp=True)        
        switch4 = self.addSwitch('s4',stp=True)        
        host1 = self.addHost('h1', cpu=.25, mac='00:00:00:00:00:01')        
        host2 = self.addHost('h2', cpu=.25)
        self.addLink(host1, switch1, bw=10, delay='5ms', loss=0, use_htb=True)        
        self.addLink(host2, switch2, bw=10, delay='5ms', loss=0, use_htb=True)
        self.addLink(switch1, switch3, bw=10, delay='5ms', loss=0.1, use_htb=True)        
        self.addLink(switch1, switch4, bw=10, delay='5ms', loss=0, use_htb=True)
        self.addLink(switch2, switch4, bw=10, delay='5ms', loss=0, use_htb=True)

def Test():
    topo = SingleSwitchTopo()
    net = Mininet( topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=False )
    net.start()    
    info( "Dumping host connections\n" )    
    dumpNodeConnections(net.hosts)
    info( "Testing bandwidth between h1 and h4\n" )    
    h1, h2 = net.getNodeByName('h1', 'h2')    
    s1, s2 = net.getNodeByName('s1', 's2')
    CLI(net)    
    net.stop()

if __name__ == '__main__':    
    # setLogLevel( 'debug' )    
    setLogLevel('info')    
    # Prevent test_simpleperf from failing due to packet loss   
    Test()