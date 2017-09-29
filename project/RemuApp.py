import kivy

from RemuTCP.RemuTCP import RemuTCP
from GUI.GUIFactory import GUIFactory
from kivy.app import App
from kivy.lang.builder import Builder
from Domain.Message import Message

"""
    HANDLES THE NAMING OF SLAVES AND MASTER AND THE MESSAGE SENT
    
    Called by Main.py. and uses GUIFactory.py to add the actual functionalities to the layouts,
    produces by the Buildkv
"""
kivy.require('1.10.0')



BuildKV = Builder.load_file('GUI/remu.kv')

class RemuApp(App):
    guimaker = GUIFactory()
    isMaster = False
    slaves = None
    master = None


    """
    The building method uses the GUI/remu.kv file that produces the look of the requested layouts
    and GUIFactory that adds the functionalities to those layouts.
    """

    def build(self):
        self.guimaker.set_parent(self)
        return BuildKV
    """
    RemuApp sets slaves and master with boolean parameter isMaster
    """
    def set_master(self):
        self.isMaster = True

    def set_slave(self):
        self.isMaster = False
        self.master = RemuTCP(self)

    """
    You can add slaves to master by using REMUTCP.py 
    """
    def add_slave(self, slave_address):
        self.slaves = RemuTCP(self, True, slave_address)
        print("Slave added")

    """
    Sends a message from master to slave using imported Message class.  
    """
    def send_msg(self, msg_address, data):
        msg = Message()
        msg.set_field("address", msg_address)
        msg.set_field("text", data)
        msg.set_field("isMaster", self.isMaster)
        self.slaves.send_message(msg)
    """
    Opens the message. If the message is sent by master the the first branch activates and we press the button in slave layout
    """
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

    def close_connections(self):
        if self.master:
            self.master.stop_listening()