import sys

from Domain.Message import Message


#############################################
"""
 Patch-around to enable Twisted with Kivy,
 Kivy's latest release prevents from using a
 method in Twisted that has been fixed for
 Python 3
"""
realVersionInfo = sys.version_info


class DummyVersionInfo(object):
    def __getitem__(self, index):
        sys.version_info = realVersionInfo
        return 2


sys.version_info = DummyVersionInfo()


try:
    from kivy.support import install_twisted_reactor
    install_twisted_reactor()
except:
    pass

##############################################
"""
HANDLES THE CONNECTION MAKING BETWEEN MASTER AND SLAVE

by using the ClientFactory and Protocol classes from Twisted.
"""
from twisted.internet import reactor, protocol


class RemuProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.connection.on_connection(self.transport)

    def dataReceived(self, data):
        print("data:", data)
        response = self.factory.connection.handle_message(data.decode('utf-8'))
        if response:
            self.transport.write(response.encode('utf-8'))


class RemuProtocolFactory(protocol.ClientFactory):
    protocol = RemuProtocol

    def __init__(self, connection):
        self.connection = connection

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.')
        self.connection.parent.on_connection_lost()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed.')
"""
In constructor checks if the computer is a master, if yes it starts to commect to slave,
if no it is thus a slave and starts listening.
"""

class RemuTCP:

    def __init__(self, parent=None, master=False, address=None, port=8000):
        self.connection = None
        self.address = None
        self.listener = None
        self.port = port
        self.parent = parent
        self.is_master = master
        if master:
            self.address = address
            self.connect_to_slave(port)
        else:
            self.listen_to_master(port)

    """
    The slave stops listening to the port in question
    """
    def stop_listening(self):
        self.listener.stopListening()

    def set_parent(self, parent):
        self.parent = parent

    """
    The constructor calls when computer is indentified as master. Uses the imported reactor to make a TCP connection
    to slave and sends the message to port 8000
    """

    def connect_to_slave(self, port):
        reactor.connectTCP(self.address, port, RemuProtocolFactory(self))
    """
    The constructor calls when computer is indentified as a slave. Uses imported reactor to start listening for TCP connection 
    possibility in port 8000
    """

    def listen_to_master(self, port):
        print("listening")
        self.listener = reactor.listenTCP(port, RemuProtocolFactory(self))

    """
    Sets the parameter connection to point to the succesfully made connection
    
    """
    def on_connection(self, connection):
        print("Connected successfully!")
        self.connection = connection
        full_address = self.address if self.address else "localhost"
        full_address += ':' + str(self.port)
        self.parent.connection_established(full_address)
        if not self.is_master:
            self.parent.close_UDP_connection()

    """
    Sends the message given as parameter if the connection is valid and on
    """
    def send_message(self, msg):
        if msg and self.connection:
            self.connection.write(msg.to_json().encode('utf-8'))
    """
    Makes a Message from the json message and adds a sender field. 
    """
    def handle_message(self, json_msg):
        msg = Message(json_msg)
        msg.set_field("sender", self.connection.getPeer().host)
        response = self.parent.handle_message(msg)
        if response:
            response.set_field("address", msg.get_field("sender"))
            print("response to json:", response.fields)
            return response.to_json()
        return None

    def end_connection(self):
        if self.listener:
            self.stop_listening()
        if self.connection:
            self.connection.loseConnection()