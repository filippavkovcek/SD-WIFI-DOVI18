 #!/usr/bin/python
#Matej Kuzma, topologia 1, 6 AP, 2 stanice
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

    info("*** Creating topology\n")
    #definicie stanic
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8') 
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8')
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.5/8')

    #definicie AP
    #first row
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1',position='50,100,0', range='70')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='2',position='150,100,0', range='70')
    ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='3',position='250,100,0', range='70')
    #second row
    ap4 = net.addAccessPoint('ap4', ssid='ap4-ssid', mode='g', channel='4',position='50,200,0', range='70')
    ap5 = net.addAccessPoint('ap5', ssid='ap5-ssid', mode='g', channel='5',position='150,200,0', range='70')
    ap6 = net.addAccessPoint('ap6', ssid='ap6-ssid', mode='g', channel='6',position='250,200,0', range='70')
    #definicie switchov
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
    net.addLink(ap5, s1)
    net.addLink(ap6, s1)

    net.plotGraph(max_x=graphDimensionSize, max_y=graphDimensionSize)

    net.startMobility(time=0, repetitions=1)

    net.mobility(sta1, 'start', time=0, position='150, 75, 0')
    net.mobility(sta1, 'stop', time=seconds, position='150, 75, 0')

    net.mobility(sta2, 'start', time=0, position='20 , 150 , 0')
    net.mobility(sta3, 'start', time=0, position='10, 150, 0')
    net.mobility(sta4, 'start', time=0, position='30, 150, 0')

    net.mobility(sta2, 'stop', time=seconds, position='280, 150, 0') 
    net.mobility(sta3, 'stop', time=seconds, position='270, 150, 0')
    net.mobility(sta4, 'stop', time=seconds, position='290, 150, 0')

    net.stopMobility(time=seconds)

    info("*** Starting network\n")
    net.build()
    c1.start()
    s1.start([c1])
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])
    ap6.start([c1]) 

    #STARTING IPERF
    info("*** Starting IPERF\n")
    serverBW = [None] * seconds
    clientBW = [None] * seconds

    #iperf server
    sta1.popen("iperf -s -p 5001 > ./iperf_server2.txt", shell=True)
    sta1.popen("iperf -s -p 5002 > ./iperf_server3.txt", shell=True)
    sta1.popen("iperf -s -p 5003 > ./iperf_server4.txt", shell=True)

    #iperf clients
    sta2.popen("iperf -c %s -U -p 5001 -t %s -i 1 > ./iperf_client2.txt" % (sta1.IP(), seconds), shell=True)
    sta3.popen("iperf -c %s -U -p 5002 -t %s -i 1 > ./iperf_client3.txt" % (sta1.IP(), seconds), shell=True)
    sta2.popen("iperf -c %s -U -p 5003 -t %s -i 1 > ./iperf_client4.txt" % (sta1.IP(), seconds), shell=True)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

    os.system("cat ./iperf_client.txt")
    os.system("cat ./iperf_client.txt | grep \"/sec\" | rev | cut -d ' ' -f 5,2 | rev")

if __name__ == '__main__':
    setLogLevel('info')
    topology()
