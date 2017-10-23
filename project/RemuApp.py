import ipaddress

import kivy

from RemuTCP.RemuTCP import RemuTCP
from GUI.GUIFactory import GUIFactory
from kivy.app import App
from kivy.lang.builder import Builder
from Domain.Slave import Slave
from Domain.Master import Master

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
    Sets the given object as service mode
    
    servicemode: the object to set as master or slave
    """
    def set_servicemode(self, servicemode, isMaster):
        self.isMaster = isMaster
        self.servicemode = servicemode

    """
    Get the app's Master
    Creates a new Master object as self.servicemode if not set
    
    layout: the layout to bind with self.servicemode
    """
    def get_master(self, layout):
        if self.servicemode is None:
            self.create_servicemode(layout, True)

        return self.servicemode

    """
    Get the app's Slave
    Creates a new Slave object as self.servicemode if not set

    layout: the layout to bind with self.servicemode
    """
    def get_slave(self, layout):
        if self.servicemode is None:
            self.create_servicemode(layout, False)

        return self.servicemode

    """
    Creates a new service object and sets it in the self.servicemode
    
    layout: the layout to bind with self.servicemode
    """
    def create_servicemode(self, layout, is_master):
        if is_master:
            new_master = Master(layout)
            self.set_servicemode(new_master, True)
        else:
            new_slave = Slave(layout)
            self.set_servicemode(new_slave, False)

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
