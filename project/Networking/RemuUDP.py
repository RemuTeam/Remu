from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from socket import SOL_SOCKET, SO_BROADCAST
import sys



class EchoClientDatagramProtocol(DatagramProtocol):
    strings = [
        "Hello, world!",
        "What a fine day it is.",
        "Bye-bye!"
    ]

    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        #self.transport.connect('<broadcast>', 8000)
        self.sendDatagram()

    def sendDatagram(self):
        if len(self.strings):
            datagram = self.strings.pop(0)
            self.transport.write(datagram.encode(), ('<broadcast>', 8000)) # <- write to broadcast address here
            print("message sent")
        else:
            reactor.stop()
            print("we're done go home")


    def datagramReceived(self, datagram, host):
        print('Datagram received: %s'%datagram)
        self.sendDatagram()


def main():
    protocol = EchoClientDatagramProtocol()
    #0 means any port

    t=reactor.listenUDP(8000, protocol)
    t.setBroadcastAllowed(True)

    reactor.run()


if __name__ == '__main__':
   main()
