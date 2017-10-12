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

    def __init__(self, **kwargs):
        super(RemuApp, self).__init__(**kwargs)
        self.guimaker = GUIFactory()
        self.isMaster = False
        self.slaves = None
        self.master = None
        self.servicemode = None

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
    def set_master(self, master):
        self.isMaster = True
        self.servicemode = master

    def set_slave(self, slave):
        self.isMaster = False
        self.servicemode = slave

    """
    Ends the presentation by calling the current servicemode's end_presentation method.
    slave servicemode end_presentation not yet implemented
    """
    def end_presentation(self):
        self.servicemode.end_presentation()

    """
        Closes all established connections and stops listening to any future connection attempts.
    """

    def close_connections(self):
        if self.servicemode:
            self.servicemode.close_connections()
