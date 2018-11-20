 #!/usr/bin/python

'Setting the position of nodes and providing mobility'

import sys

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1',
                             position='50,100,0', range='50')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='2',
                            position='150,100,0', range='50')
    s1 = net.addSwitch('s1');

    c1 = net.addController('c1', controller=Controller)

    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, s1)
    net.addLink(ap2, s1)

    net.plotGraph(max_x=200, max_y=200)

    net.startMobility(time=0, repetitions=1)

    net.mobility(sta1, 'start', time=2, position='50.0,75.0,0.0')
    net.mobility(sta1, 'stop', time=22, position='50.0,80.0,0.0')
    net.mobility(sta2, 'start', time=2, position='50.0,80.0,0.0')
    net.mobility(sta2, 'stop', time=22, position='175.0,75.0,0.0')

    net.stopMobility(time=23)

    info("*** Starting network\n")
    net.build()
    c1.start()
    s1.start([c1])
    ap1.start([c1])
    ap2.start([c1])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()   
