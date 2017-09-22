import sys

from Domain.Message import Message


#############################################
# Patch-around to enable Twisted with Kivy,
# Kivy's latest release prevents from using a
# method in Twisted that has been fixed for
# Python 3

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


from twisted.internet import reactor, protocol


class RemuProtocol(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        response = self.factory.app.handle_message(data.decode('utf-8'))
        if response:
            self.transport.write(response.encode('utf-8'))


class RemuProtocolFactory(protocol.ClientFactory):
    protocol = RemuProtocol

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        print('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.')

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed.')


class RemuTCP:
    connection = None
    address = None
    port = None

    def __init__(self, app, master=False, address=None, port=8000):
        self.app = app
        if master:
            self.address = address
            self.connect_to_slave(port)
        else:
            self.listen_to_master(port)

    def stop_listening(self):
        self.port.stopListening()

    def connect_to_slave(self, port):
        reactor.connectTCP(self.address, port, RemuProtocolFactory(self))

    def listen_to_master(self, port):
        print("listening")
        self.port = reactor.listenTCP(port, RemuProtocolFactory(self))

    def on_connection(self, connection):
        print("Connected successfully!")
        self.connection = connection

    def send_message(self, msg):
        if msg and self.connection:
            self.connection.write(msg.to_json().encode('utf-8'))

    def handle_message(self, json_msg):
        msg = Message(json_msg)
        msg.set_field("sender", self.connection.getPeer().host)
        response = self.app.handle_message(msg)
        if response:
            response.set_field("address", msg.get_field("sender"))
            return response.to_json()
        return None