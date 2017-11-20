import kivy
import Networking.IP as IP
from Networking.RemuTCP import RemuTCP
from GUI.GUIFactory import GUIFactory #ÄLÄ POISTA
from kivy.app import App
from kivy.lang.builder import Builder
from Domain.Slave import Slave
from Domain.Master import Master
from Domain.Presentation import Presentation

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
        self.isMaster = False
        self.slaves = None
        self.servicemode = None
        self.localip = IP.get_local_ip_address()

    def build(self):
        """
        The building method uses the GUI/remu.kv file that produces the look of the requested layouts
        and GUIFactory that adds the functionalities to those layouts.
        """
        return BuildKV

    def set_servicemode(self, servicemode, isMaster):
        """
        Sets the given object as service mode

        servicemode: the object to set as master or slave
        """
        self.isMaster = isMaster
        self.servicemode = servicemode
        if self.isMaster:
            self.servicemode.start_udp_listening()
            self.servicemode.start_ftp_server('./media', 8005)

    def get_master(self, layout):
        """
        Get the app's Master
        Creates a new Master object as self.servicemode if not set

        layout: the layout to bind with self.servicemode
        """
        if self.servicemode is None:
            self.create_servicemode(layout, True)

        return self.servicemode

    def get_slave(self, layout):
        """
        Get the app's Slave
        Creates a new Slave object as self.servicemode if not set

        layout: the layout to bind with self.servicemode
        """
        if self.servicemode is None:
            self.create_servicemode(layout, False)

        return self.servicemode

    def create_servicemode(self, layout, is_master):
        """
        Creates a new service object and sets it in the self.servicemode

        layout: the layout to bind with self.servicemode
        """
        if is_master:
            new_master = Master(layout)
            self.set_servicemode(new_master, True)
        else:
            new_slave = Slave(layout)
            new_slave.set_master_connection(RemuTCP(new_slave))
            self.set_servicemode(new_slave, False)

    def end_presentation(self):
        """
        Ends the presentation by calling the current servicemode's end_presentation method.
        slave servicemode end_presentation not yet implemented
        """
        if self.isMaster:
            self.servicemode.end_presentation()

    def reset_servicemode(self):
        self.end_presentation()
        self.close_connections()
        print("I've done reset 'em all, self.servicemode was " + str(self.servicemode))
        self.servicemode = None
        print("and is now " + str(self.servicemode))

    def close_connections(self):
        """
        Closes all established connections and stops listening to any future connection attempts.
        """
        if self.servicemode:
            self.servicemode.close_all_connections()

    def init_presentation(self):
        #self.servicemode.set_presentation(Presentation())
        pass
