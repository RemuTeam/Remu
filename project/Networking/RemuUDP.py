from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from kivy.app import App
import kivy.clock
import Networking.IP as IP

from socket import SOL_SOCKET, SO_BROADCAST

DEFAULT_PORT_NUMBER = 8555


class EchoClientDatagramProtocol(DatagramProtocol):
    """
    Protocol that defines the UDP protocol used in the beaconing and datagram traffic.
    """

    strings = [
        "Hello, world!",
        "What a fine day it is.",
        "Bye-bye!"
    ]

    def __init__(self, is_slave=False, udplistener=None):
        super(EchoClientDatagramProtocol, self).__init__()
        self.is_slave = is_slave
        self.udplistener = udplistener

    def sendDatagram(self, dt=None):
        """
        Sends the beaconing signal as a broadcast.
        """
        self.transport.write("connect to me".encode(), ('<broadcast>', DEFAULT_PORT_NUMBER))
        print("message sent")
        address = App.get_running_app().localip

        stop = address.rfind('.')
        base = address[:stop]
        bcast = base + ".255"
        self.transport.write("connect to me".encode(), (bcast, DEFAULT_PORT_NUMBER))
        """
        for i in range(1, 255):
            address = base + '.' + str(i)
            self.transport.write("connect to me".encode(), (address, DEFAULT_PORT_NUMBER))
            print('sent', address)
        """

    def startProtocol(self):
        """
        Starts the protocol for UDP connections
        """
        self.transport.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        if self.is_slave:
            self.event = kivy.clock.Clock.schedule_interval(self.sendDatagram, 8)

    def stopProtocol(self):
        """
        Stops broadcasting and closes the socket used for the transport
        """
        if self.transport:
            self.transport.stopListening()
            self.transport.socket.close()

    def datagramReceived(self, datagram, host):
        """
        Is called when a datagram is received. If master receives a UDP datagram, it tries to connect to the sender.
        """
        if not self.is_slave:
            self.udplistener.master.add_slave(host[0])
        print('Datagram received: %s' % datagram.decode('utf-8'))
        print(host)


class Beacon:
    """
    Beacons are created when the Slave is initialized. Handles slave's UDP packets, and broadcast a beacon signal across the network.
    """

    def __init__(self):
        self.transport = None
        self.protocol = None

    def stop_beaconing(self):
        """
        Cancels beaconing and closes the used port.
        """
        print("Stopping beacon")
        if self.protocol is not None:
            self.protocol.event.cancel()
            #self.protocol.stopProtocol()
            self.protocol = None

    def start_beaconing(self):
        """
        Starts broadcasting the beacon signal to all ports.
        """
        print("Starting beacon")
        self.protocol = EchoClientDatagramProtocol(True, self)
        #0 means any port

        self.transport = reactor.listenUDP(0, self.protocol)
        self.transport.setBroadcastAllowed(True)


class MasterUDPListener:
    """
    MasterUDPListener is created when Master is initialized, and it starts listening to slave beacons
    """

    def __init__(self, master):
        self.master = master
        self.protocol = None
        self.transport = None

    def listen_for_beacons(self):
        """
        Called when the MasterUDPListener is initialized. Starts the protocol for listening for the beacon slaves
        """
        print("Starting listening on beacons")
        self.protocol = EchoClientDatagramProtocol(False, self)
        self.transport = reactor.listenUDP(DEFAULT_PORT_NUMBER, self.protocol)
        self.transport.setBroadcastAllowed(True)

    def stop_listening_to_beacons(self):
        """
        Called when the Master stops receiving UDP datagrams. Stops listening to slave beacons and stops the protocol
        """
        print("Stopping listening")
        if self.protocol is not None:
            self.protocol.stopProtocol()
            self.protocol = None
