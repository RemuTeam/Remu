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
    Set Master object as service mode
    
    master: the object to set as master
    """
    def set_master(self, master):
        self.isMaster = True
        self.servicemode = master

    """
    Set Slave object as service mode
    
    slave: the object to set as slave
    """
    def set_slave(self, slave):
        self.isMaster = False
        self.servicemode = slave

    """
    Get the app's Master
    Creates a new Master object as self.servicemode if not set
    
    layout: the layout to bind with self.servicemode
    """
    def get_master(self, layout):
        if self.servicemode is None:
            self.__create_master(layout)

        return self.servicemode

    """
    Get the app's Slave
    Creates a new Slave object as self.servicemode if not set

    layout: the layout to bind with self.servicemode
    """
    def get_slave(self, layout):
        if self.servicemode is None:
            self.__create_slave(layout)

        return self.servicemode

    """
    Creates a new Master object and sets it as self.servicemode
    
    layout: the layout to bind with self.servicemode
    """
    def __create_master(self, layout):
        new_master = Master(layout)
        self.set_master(new_master)

    """
    Creates a new Slave object and sets it as self.servicemode

    layout: the layout to bind with self.servicemode
    """
    def __create_slave(self, layout):
        new_slave = Slave(layout)
        new_slave.set_master_connection(RemuTCP())
        self.set_slave(new_slave)

    """
    Ends the presentation by calling the current servicemode's end_presentation method.
    slave servicemode end_presentation not yet implemented
    """
    def end_presentation(self):
        if self.isMaster:
            self.servicemode.end_presentation()

    def reset_servicemode(self):
        self.end_presentation()
        self.close_connections()
        print("I've done reset 'em all, self.servicemode was " + str(self.servicemode))
        self.servicemode = None
        print("and is now " + str(self.servicemode))

    """
        Closes all established connections and stops listening to any future connection attempts.
    """

    def close_connections(self):
        if self.servicemode:
            self.servicemode.close_connections()
