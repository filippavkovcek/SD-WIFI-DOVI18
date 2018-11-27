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

    net.mobility(sta1, 'start', time=0, position='50.0,75.0,0.0')
    net.mobility(sta1, 'stop', time=seconds, position='50.0,80.0,0.0')
    net.mobility(sta2, 'start', time=0, position='50.0,80.0,0.0')
    net.mobility(sta2, 'stop', time=seconds, position='175.0,75.0,0.0')

    net.stopMobility(time=seconds)

    info("*** Starting network\n")
    net.build()
    c1.start()
    s1.start([c1])
    ap1.start([c1])
    ap2.start([c1])


    #STARTING IPERF
    info("*** Starting IPERF\n")
    serverBW = [None] * seconds
    clientBW = [None] * seconds

    ap1.popen("iperf -s -p 5001 > ./iperf_server.txt")
    ap2.popen("iperf -c %s -p 5001 -t %s -i 1 > ./iperf_client.txt" % (ap1.IP(), seconds), shell=True)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

    os.system("cat ./iperf_client.txt")
    os.system("cat ./iperf_client.txt | grep \"/sec\" | rev | cut -d ' ' -f 5,2 | rev")

if __name__ == '__main__':
    setLogLevel('info')
    topology()   
