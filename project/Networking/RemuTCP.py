import sys
import kivy
from kivy.app import App
from Domain.Message import Message
from kivy.logger import Logger

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

if kivy.__version__ != '1.10.1.dev0':
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
        Logger.debug("RemuTCP: data received")
        Logger.debug("RemuTCP: %s", str(data))
        response = self.factory.connection.handle_message(data.decode('utf-8'))
        if response:
            self.transport.write(response.encode('utf-8'))

    def connectionLost(self, reason):
        self.factory.connection.connection_terminated()


class RemuProtocolFactory(protocol.ClientFactory):
    protocol = RemuProtocol

    def __init__(self, connection):
        self.connection = connection

    def startedConnecting(self, connector):
        Logger.info("RemuTCP: Started to connect")

    def clientConnectionLost(self, connector, reason):
        Logger.info("RemuTCP: Lost connection.")
        self.connection.parent.on_connection_lost()

    def clientConnectionFailed(self, connector, reason):
        Logger.info("RemuTCP: Connection failed.")




class RemuTCP:

    def __init__(self, parent=None, master=False, address=None, port=8000):
        self.connection = None
        self.address = None
        self.listener = None
        self.port = port
        self.parent = parent
        self.is_master = master
        self.address = address

    def stop_listening(self):
        """
        The slave stops listening to the port in question
        """
        if self.listener:
            self.listener.stopListening()

    def connection_terminated(self):
        if not self.is_master:
            self.parent.beacon.start_beaconing()

    def run(self):
        """
        Checks if the computer is a master, if yes it starts to commect to slave,
        if no it is thus a slave and starts listening.
        """
        if self.is_master:
            self.connect_to_slave(self.port)
        else:
            self.listen_to_master(self.port)

    def set_parent(self, parent):
        self.parent = parent

    def connect_to_slave(self, port):
        """
        The constructor calls when computer is indentified as master. Uses the imported reactor to make a TCP connection
        to slave and sends the message to port 8000
        """
        reactor.connectTCP(self.address, port, RemuProtocolFactory(self))

    def listen_to_master(self, port):
        """
        The constructor calls when computer is indentified as a slave. Uses imported reactor to start listening for TCP
        connection possibility in port 8000
        """
        Logger.info("RemuTCP: Listening")
        self.listener = reactor.listenTCP(port, RemuProtocolFactory(self))

    def on_connection(self, connection):
        """
        Sets the parameter connection to point to the succesfully made connection
        """
        Logger.info("RemuTCP: Connected successfully!")
        self.connection = connection
        full_address = self.address if self.address else "localhost"
        full_address += ':' + str(self.port)
        self.parent.connection_established(full_address)
        if not self.is_master:
            self.parent.close_UDP_connection()

    def send_message(self, msg):
        """
        Sends the message given as parameter if the connection is valid and on
        """
        if msg and self.connection:
            name = self.__get_name()
            msg.set_field("name", name)

            self.connection.write(msg.to_json().encode('utf-8'))

    def handle_message(self, json_msg):
        """
        Makes a Message from the json message and adds a sender field.
        """
        msg = Message(json_msg)
        msg.set_field("sender", self.connection.getPeer().host)
        response = self.parent.handle_message(msg)
        if response:
            response.set_field("name", self.__get_name())
            response.set_field("address", msg.get_field("sender"))
            Logger.debug("RemuTCP: response to json")
            Logger.debug("RemuTCP: %s", str(response.fields))
            return response.to_json()
        return None

    def end_connection(self):
        if self.listener:
            self.stop_listening()
        if self.connection:
            self.connection.loseConnection()

    def __get_name(self):
        app = App.get_running_app()
        name = "test"
        if app is not None:
            name = app.config.get("name")
        return name