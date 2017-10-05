import ipaddress

import kivy

from RemuTCP.RemuTCP import RemuTCP
from GUI.GUIFactory import GUIFactory
from kivy.app import App
from kivy.lang.builder import Builder
from Domain.Slave import Slave

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
        self.master = RemuTCP(Slave())


    """
        Closes all established connections and stops listening to any future connection attempts.
    """

    def close_connections(self):
        if self.master:
            self.master.stop_listening()
            if self.master.connection:
                self.master.connection.loseConnection()
        if self.slaves and self.slaves.connection:
            self.slaves.connection.loseConnection()
