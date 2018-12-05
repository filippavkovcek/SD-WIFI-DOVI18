 #!/usr/bin/python

'Setting the position of nodes and providing mobility'

import sys
import os
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():

    #number of seconds to run test
    seconds = 10
    graphDimensionSize = 300

    "Create a network."
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")

    #stations
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    sta3 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')

    #acces points
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1',position='100, 100, 0', range='100')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='2',position='100, 200, 0', range='100')
    ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='3',position='200, 100, 0', range='100')
    ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='g', channel='4',position='200, 200, 0', range='100')

    #switches
    s1 = net.addSwitch('s1');

    c1 = net.addController('c1', controller=Controller)

    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, s1)
    net.addLink(ap2, s1)
    net.addLink(ap3, s1)
    net.addLink(ap4, s1)

    net.plotGraph(max_x=graphDimensionSize, max_y=graphDimensionSize)

    net.startMobility(time=0, repetitions=1)

    net.mobility(sta1, 'start', time=0, position='200, 205, 0')
    net.mobility(sta1, 'stop', time=seconds, position='200, 205, 0')

    net.mobility(sta2, 'start', time=0, position='20, 105, 0')
    net.mobility(sta2, 'stop', time=seconds, position='270, 105, 0')

    net.mobility(sta2, 'start', time=0, position='105, 20, 0')
    net.mobility(sta2, 'stop', time=seconds, position='105, 280, 0')

    net.stopMobility(time=seconds)

    info("*** Starting network\n")
    net.build()
    c1.start()
    s1.start([c1])
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])

    #STARTING IPERF
    info("*** Starting IPERF\n")
    serverBW = [None] * seconds
    clientBW = [None] * seconds

    sta1.popen("iperf -s -p 5001 > ./iperf_server1.txt", shell=True)
    sta1.popen("iperf -s -p 5002 > ./iperf_server2.txt", shell=True)
    sta2.popen("iperf -c %s -U -p 5001 -t %s -i 1 > ./iperf_client1.txt" % (sta1.IP(), seconds), shell=True)
    sta3.popen("iperf -c %s -U -p 5002 -t %s -i 1 > ./iperf_client2.txt" % (sta1.IP(), seconds), shell=True)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

    os.system("cat ./iperf_client.txt")
    os.system("cat ./iperf_client.txt | grep \"/sec\" | rev | cut -d ' ' -f 5,2 | rev")

if __name__ == '__main__':
    setLogLevel('info')
    topology()
