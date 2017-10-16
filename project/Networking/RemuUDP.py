from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import kivy.clock

from socket import SOL_SOCKET, SO_BROADCAST
import sys



class EchoClientDatagramProtocol(DatagramProtocol):
    strings = [
        "Hello, world!",
        "What a fine day it is.",
        "Bye-bye!"
    ]

    def sendDatagram(self, dt=None):
        if len(self.strings):
            #datagram = self.strings.pop(0)
            self.transport.write("connect to me".encode(), ('<broadcast>', 8000)) # <- write to broadcast address here
            print("message sent")
        else:
            #reactor.stop()
            print("we're done go home")

    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        #self.transport.connect('<broadcast>', 8000)
        kivy.clock.Clock.schedule_interval(self.sendDatagram, 2)
        #self.sendDatagram()




    def datagramReceived(self, datagram, host):
        print('Datagram received: %s' % datagram.decode('utf-8'))
        print(host)
        #self.sendDatagram()

class Beacon:

    def main(self):
        protocol = EchoClientDatagramProtocol()
        #0 means any port

        t=reactor.listenUDP(8000, protocol)
        t.setBroadcastAllowed(True)

        #reactor.run()


#if __name__ == '__main__':
   #main()
