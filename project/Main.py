
import kivy
kivy.require('1.10.0')

from GUI.GUIFactory import GUIFactory
from RemuTCP.RemuTCP import RemuTCP
from GUI.GUIFactory import GUIFactory
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

import sys

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


from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic


# Initializes connections between master and slave
# as well as handles the messages sent
class RemuProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        print(line.decode('ascii'))


# Keeps track of the connections made by the slaves and clients
class RemuFactory(protocol.Factory):
    def __init__(self, app):
        self.clients = set()
        self.app = app

    def buildProtocol(self, addr):
        return RemuProtocol(self)


BuildKV = Builder.load_file("remu.kv")

class RemuApp(App):
    guimaker = GUIFactory()
    isMaster = False
    slaves = None
    master = None

    def build(self):
        self.guimaker.set_parent(self)
        return BuildKV

    def set_master(self):
        self.isMaster = True

    def set_slave(self):
        self.isMaster = False
        self.master = RemuTCP()

    def add_slave(self, slave_address):
        self.slaves = RemuTCP(True, slave_address)
        print("Slave added")

    def send_msg(self, msg_address, data):
        self.slaves.send_message(data)


if __name__ == '__main__':
    args = sys.argv

    address = ''
    master = False

    if len(args) > 1:
        master = args[1] == 'master'
        address = args[2]

    RemuApp().run()
