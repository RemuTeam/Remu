import sys


#############################################
# Patch-around to enable Twisted with Kivy,
# Kivy's latest release prevents from using a
# method in Twisted

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


class RemuSlave(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data.decode('utf-8'))



class RemuSlaveFactory(protocol.ClientFactory):
    protocol = RemuSlave

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        self.app.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        self.app.print_message('Lost connection.')

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Connection failed.')


class RemuTCP:
    connection = None

    def __init__(self):
        self.listen_to_master()

    #def build(self):
    #    #self.connect_to_server()
    #    return self

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, RemuSlaveFactory(self))

    def listen_to_master(self):
        print("listening")
        reactor.listenTCP(8000, RemuSlaveFactory(self))

    def on_connection(self, connection):
         self.print_message("Connected successfully!")
         self.connection = connection

    def send_message(self, msg):
        if msg and self.connection:
            self.connection.write(msg.encode('utf-8'))

    def print_message(self, msg):
        print("{}\n".format(msg))