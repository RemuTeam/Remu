
import kivy
import sys

from RemuTCP.RemuTCP import RemuTCP
from GUI.GUIFactory import GUIFactory
from kivy.app import App
from kivy.lang.builder import Builder
from Domain.Message import Message

kivy.require('1.10.0')


BuildKV = Builder.load_file('GUI/remu.kv')

class RemuApp(App):
    guimaker = GUIFactory()
    isMaster = False
    slaves = None
    master = None
    gui = None

    def build(self):
        self.guimaker.set_parent(self)
        return BuildKV

    def set_gui(self, gui):
        self.gui = gui;

    def set_master(self):
        self.isMaster = True

    def set_slave(self):
        self.isMaster = False
        self.master = RemuTCP(self)

    def add_slave(self, slave_address):
        self.slaves = RemuTCP(self, True, slave_address)
        print("Slave added")

    def send_msg(self, msg_address, data):
        msg = Message()
        msg.set_field("address", msg_address)
        msg.set_field("text", data)
        msg.set_field("isMaster", self.isMaster)
        self.slaves.send_message(msg)

    def handle_message(self, msg):
        if msg.get_field("isMaster"):
            self.root.get_screen(self.root.current).button_pressed()
        print(msg.fields)
        response = None
        if not self.isMaster:
            response = Message()
            response.set_field("text", "OK!")
            response.set_field("isMaster", self.isMaster)
        return response

if __name__ == '__main__':
    args = sys.argv

    address = ''
    master = False

    if len(args) > 1:
        master = args[1] == 'master'
        address = args[2]

    RemuApp().run()
