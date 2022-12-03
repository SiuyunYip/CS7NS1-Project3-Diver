#!../pj3-env/bin/python

import logging
import threading
import time
import socket
import random
import sys, getopt


class Device:

    def __init__(self, name, host, router_ip, router_port):
        self.area = None
        self.name = name
        self.host = host
        self.router_ip = router_ip
        self.router_port = router_port

    def sensorData(self, clientMsg):
        clientMsg = clientMsg.lower()
        clientMsg = clientMsg.replace(" ", "")
        clientMsg_arr = clientMsg.split(',')
        clientMsg = clientMsg_arr[1].split('/')
        sensorValue = ""
        if "temperature" in clientMsg:
            sensorValue += "Temperature," + str(random.randint(35, 40))
        if "pressure" in clientMsg:
            sensorValue += "Pressure," + str(random.randint(76, 84))
        if "speed" in clientMsg:
            sensorValue += "Speed," + str(random.randint(0, 5))
        if "surroundingtemperature" in clientMsg:
            sensorValue += "Surrounding Temperature," + str(random.randint(5, 10))
        if "bloodoxygenlevel" in clientMsg:
            sensorValue += "Blood oxygen level," + str(random.randint(80, 100))
        if "heartbeat" in clientMsg:
            sensorValue += "Heart Beat," + str(random.randint(75, 80))
        if "hydration" in clientMsg:
            sensorValue += "Hydration," + str(random.randint(69, 73))
        if "bloodsugar" in clientMsg:
            sensorValue += "Blood Sugar," + str(random.randint(89, 93))

        return sensorValue

    def discovery(self, UDPsensor, i):
        bytesToSend = str.encode("discover," + i)
        routerAddressPort = (self.router_ip, int(self.router_port))
        UDPsensor.sendto(bytesToSend, routerAddressPort)

    def pi_sensor(self, i):
        localIP = self.host
        localPort = i[0]
        bufferSize = 1024
        UDPsensor = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPsensor.bind((localIP, localPort))
        print("UDP snsor up and listening in port " + str(i[0]))
        self.discovery(UDPsensor, i[1])
        while (True):
            bytesAddressPair = UDPsensor.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = message.decode("utf-8")

            if clientMsg.startswith('discover'):
                print('Received area name: ', clientMsg)
                self.area = clientMsg.split(',')[1]
            else:
                msgToServer = "resource," + i[1] + "," + self.area + '/' + i[1] + '/' + self.sensorData(clientMsg)
                print(msgToServer)
                bytesToSend = str.encode(msgToServer)
                UDPsensor.sendto(bytesToSend, address)


def main(argv):
    host = ''
    router_ip = ''
    router_port = ''

    try:
        opts, args = getopt.getopt(argv, "ho:i:p:", ["host=", "router_ip=", "router_port="])
    except getopt.GetoptError:
        print("use command line:", "device.py -o <host> -i <router ip> -p <router port>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("use command line:", "device.py -o <host> -i <router ip> -p <router port>")
            sys.exit()
        elif opt in ("-o", "--host"):
            host = arg
        elif opt in ("-i", "--router_ip"):
            router_ip = arg
        elif opt in ("-p", "--router_port"):
            router_port = arg
    if host == '' or router_ip == '' or router_port == '':
        print("use command line:", "device.py -o <host> -i <router ip> -p <router port>")
        sys.exit()

    print('host: ', host)
    print('router ip: ', router_ip)
    print('router port: ', router_port)

    for i in [[33001, 'Bob'], [34001, 'Alice'], [35001, 'Eve'], [36001, 'John'], [37001, 'Ben']]:
        logging.info("Main    : create and start thread %d.", i)
        device = Device(i[1], host, router_ip, router_port)
        x = threading.Thread(target=device.pi_sensor, args=(i,))
        x.start()
        time.sleep(2)


if __name__ == '__main__':
    main(sys.argv[1:])
