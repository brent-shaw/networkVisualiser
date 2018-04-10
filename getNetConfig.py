from __future__ import absolute_import, division, print_function
import logging
import scapy.config
import scapy.layers.l2
import scapy.route
import socket
import math
import errno

def long2net(arg):
    if (arg <= 0 or arg >= 0xFFFFFFFF):
        raise ValueError("illegal netmask value", hex(arg))
    return 32 - int(round(math.log(0xFFFFFFFF - arg, 2)))


def setNotation(bytes_network, bytes_netmask):
    network = scapy.utils.ltoa(bytes_network)
    netmask = long2net(bytes_netmask)
    net = "%s/%s" % (network, netmask)
    if netmask < 16:
        return None
    return net

def scan(net, interface, timeout=1):
    output = []
    try:
        ans, unans = scapy.layers.l2.arping(net, iface=interface, timeout=timeout, verbose=False)
        for s, r in ans.res:
            line = []
            line.append(r.sprintf("%Ether.src%"))
            line.append(r.sprintf("%ARP.psrc%"))
            try:
                hostname = socket.gethostbyaddr(r.psrc)
                line.append(hostname[0])
            except socket.herror:
                pass
            output.append(line)
    except socket.error as e:
        if e.errno == errno.EPERM:
            pass
        else:
            raise
    return output
