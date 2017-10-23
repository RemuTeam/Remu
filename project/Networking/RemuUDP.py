from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import kivy.clock

from socket import SOL_SOCKET, SO_BROADCAST

DEFAULT_PORT_NUMBER = 8555


"""
Protocol that defines the UDP protocol used in the beaconing and datagram traffic.
"""
class EchoClientDatagramProtocol(DatagramProtocol):
    strings = [
        "Hello, world!",
        "What a fine day it is.",
        "Bye-bye!"
    ]

    def __init__(self, is_slave=False, udplistener = None):
        super(EchoClientDatagramProtocol, self).__init__()
        self.is_slave = is_slave
        self.udplistener = udplistener

    """
    Sends the beaconing signal as a broadcast.
    """
    def sendDatagram(self, dt=None):
        self.transport.write("connect to me".encode(), ('<broadcast>', DEFAULT_PORT_NUMBER))
        print("message sent")


    """
    Starts the protocol for UDP connections
    """
    def startProtocol(self):
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        if self.is_slave:
            self.event = kivy.clock.Clock.schedule_interval(self.sendDatagram, 2)

    """
    Stops broadcasting and closes the socket used for the transport
    """
    def stopProtocol(self):
        self.transport.setBroadcastAllowed(False)
        self.transport.stopListening()
        self.transport.socket.close()

    """
    Is called when a datagram is received. If master receives a UDP datagram, it tries to connect to the sender.
    """
    def datagramReceived(self, datagram, host):
        if not self.is_slave:
            self.udplistener.master.add_slave(host[0])
        print('Datagram received: %s' % datagram.decode('utf-8'))
        print(host)

"""
Beacons are created when the Slave is initialized. Handles slave's UDP packets, and broadcast a beacon signal across the network. 
"""
class Beacon:

    def __init__(self):
        self.transport = None
        self.protocol = None

    """
    Cancels beaconing and closes the used port.
    """
    def stop_beaconing(self):
        print("Stopping beacon")
        if self.protocol is not None:
            self.protocol.event.cancel()
            self.protocol.stopProtocol()
            self.protocol = None

    """
    Starts broadcasting the beacon signal to all ports.
    """
    def start_beaconing(self):
        print("Starting beacon")
        self.protocol = EchoClientDatagramProtocol(True, self)
        #0 means any port

        self.transport = reactor.listenUDP(0, self.protocol)
        self.transport.setBroadcastAllowed(True)

"""
MasterUDPListener is created when Master is initialized, and it starts listening to slave beacons
"""
class MasterUDPListener:

    def __init__(self):
        self.protocol = None
        self.transport = None

    """
    Called when the MasterUDPListener is initialized. Starts the protocol for listening for the beacon slaves
    """
    def listen_for_beacons(self):
        print("Starting listening on beacons")
        self.protocol = EchoClientDatagramProtocol(False, self)

        self.transport = reactor.listenUDP(DEFAULT_PORT_NUMBER, self.protocol)
        self.transport.setBroadcastAllowed(True)

    """
    Called when the Master stops receiving UDP datagrams. Stops listening to slave beacons and stops the protocol
    """
    def stop_listening_to_beacons(self):
        print("Stopping listening")
        if self.protocol is not None:
            self.protocol.stopProtocol()
            self.protocol = None
