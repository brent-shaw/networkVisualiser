from __future__ import absolute_import, division, print_function
import logging
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import errno
import networkx as nx
import matplotlib.pyplot as plt
from getNetConfig import setNotation, scan

class Networks():

    def __init__(self):
        self.networks = {}
        self.count = 0

    def addNetwork(self, name):
        self.networks.update({name: Network(name)})

    def addNodeToNet(self, networkName, nodeName):
        self.networks[networkName].addNode(nodeName)

    def addNodesToNet(self, networkName, nodes):
        for n in nodes:
            self.networks[networkName].addNode(n)

    def printNetworks(self):
        for (key, value) in self.networks.items():
            print(key)

    def getNetworks(self):
        return [value for (key, value) in self.networks.items()]


    def printNetworksAndNodes(self):
        for (key, value) in self.networks.items():
            print(key)
            value.printNodes()

    def createGraph(self):
        G=nx.Graph()

        for n in self.getNetworks():
            G.add_node(n.name)
            for ni in n.getNodes():
                G.add_edge(n.name,ni.name)
        return G

class Network():

    def __init__(self, name):
        self.nodes = {}
        self.name = name

    def addNode(self, name):
        self.nodes.update({name: Node(name)})

    def printNodes(self):
        for (key, value) in self.nodes.items():
            print('-',key)

    def getNodes(self):
        return [value for (key, value) in self.nodes.items()]

class Node():
    def __init__(self, name):
        self.name = name
        #print('Made',name)

def testSetup():
    nets = Networks()

    nets.addNetwork('Rhodes')
    nets.addNetwork('Docker0')

    nets.addNodeToNet('Rhodes', 'Pequod')

    nets.addNodeToNet('Docker0', 'Pequod')
    nets.addNodeToNet('Docker0', 'Modbus Server')
    nets.addNodeToNet('Docker0', 'Modbus Client 1')
    nets.addNodeToNet('Docker0', 'Modbus Client 2')
    nets.addNodeToNet('Docker0', 'Modbus Client 3')

    return nets

def getLocalNetwork():
    nodes = []
    for network, netmask, _, interface, address in scapy.config.conf.route.routes:
        if network == 0 or interface == 'lo' or address == '127.0.0.1' or address == '0.0.0.0':
            continue

        if netmask <= 0 or netmask == 0xFFFFFFFF:
            continue

        net = setNotation(network, netmask)

        if interface != scapy.config.conf.iface:
            continue

        stuff = []
        if net:
            stuff = scan(net, interface)

        for s in stuff:
            nodes.append(s)

    return nodes


nets = Networks()
nets.addNetwork('Net')

localNodes = [n[2].split('.')[0] for n in getLocalNetwork()]

nets.addNodesToNet('Net', localNodes)
G = nets.createGraph()
nx.draw(G, with_labels=True)
plt.show()
