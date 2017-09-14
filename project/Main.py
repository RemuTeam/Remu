
import kivy
kivy.require('1.10.0')

from GUI.GUIFactory import GUIFactory
from RemuTCP.RemuTCP import RemuTCP
from kivy.app import App

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


from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic


class RemuProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        print(line.decode('ascii'))


class RemuFactory(protocol.Factory):
    def __init__(self, app):
        self.clients = set()
        self.app = app

    def buildProtocol(self, addr):
        return RemuProtocol(self)


class ReMuSlaveApp(App):

    guimaker = GUIFactory()
    isMaster = False
    connection = None

    def build(self):
        self.connection = RemuTCP()
        while True:
            msg = input("> ")
            if not input:
                break;
            self.connection.send_message(msg)
        return self.guimaker.getGUI(self.isMaster)

class ReMuMasterApp(App):

    guimaker = GUIFactory()
    isMaster = True
    slaves = {}

    def __init__(self, address):
        self.slaves[address] = RemuTCP(True, address)
        

    def build(self):
        while True:
            msg = input("> ")
            if not input:
                break;
            self.slaves[address].send_message(msg)
        return self.guimaker.getGUI(self.isMaster)


if __name__ == '__main__':
    args = sys.argv

    address = ''
    master = False

    if len(args) > 1:
        master = args[1] == 'master'
        address = args[2]

    if master:
        ReMuMasterApp(address).run()
    else:
        ReMuSlaveApp().run()
