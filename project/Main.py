
import kivy
kivy.require('1.10.0')

from GUI.GUIFactory import GUIFactory
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

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


class RemuApp(App):

    guimaker = GUIFactory()
    isMaster = False

    def build(self):
        print('lol')
        endpoints.serverFromString(reactor, "tcp:1025:interface=128.214.166.145").listen(RemuFactory(self))
        return self.guimaker.getMasterSwitchLayout()


if __name__ == '__main__':
    RemuApp().run()
