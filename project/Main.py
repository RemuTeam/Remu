import kivy
kivy.require('1.1.0')

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

import sys

#############################################
# Patch-around to enable Twisted with Kivy,
# Kivy's latest release prevents from using a
# method in Twisted

realVersionInfo=sys.version_info

class DummyVersionInfo(object):
    def __getitem__(self, index):
        sys.version_info=realVersionInfo
        return 2
sys.version_info=DummyVersionInfo()


try:
    from kivy.support import install_twisted_reactor
    install_twisted_reactor()
except:
    pass

##############################################

from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic


class MyButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)

    def on_press(self):
        self.source = 'a.jpg'

    def on_release(self):

        self.source = ''

    def on_message(self):
        self.on_press()


class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        print(line.decode('ascii'))
        self.factory.app.button.on_message()


class PubFactory(protocol.Factory):
    def __init__(self, app):
        self.clients = set()
        self.app = app

    def buildProtocol(self, addr):
        return PubProtocol(self)


class MyApp(App):
    button = None

    def build(self):
        endpoints.serverFromString(reactor, "tcp:1025:interface=128.214.166.145").listen(PubFactory(self))
        self.button = MyButton()
        return self.button



if __name__ == '__main__':
    MyApp().run()
