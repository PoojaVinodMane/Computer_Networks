
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller

class LoadBalancerTopology(Topo):
    def build(self):
        # Create hosts
        client = self.addHost('client', ip='10.0.0.1')
        lb = self.addHost('lb', ip='10.0.0.100')  # Load balancer
        server1 = self.addHost('server1', ip='10.0.0.2')
        server2 = self.addHost('server2', ip='10.0.0.3')
        server3 = self.addHost('server3', ip='10.0.0.4')

        # Add a switch
        switch = self.addSwitch('s1')

        # Connect hosts to the switch
        self.addLink(client, switch)
        self.addLink(lb, switch)
        self.addLink(server1, switch)
        self.addLink(server2, switch)
        self.addLink(server3, switch)

topos = {'loadbalancer': (lambda: LoadBalancerTopology())}

