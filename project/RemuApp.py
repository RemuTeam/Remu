import kivy
import Networking.IP as IP
from Networking.RemuTCP import RemuTCP
from GUI.GUICore import RemuSM, SwitchLayout, InfoLayout #ÄLÄ POISTA
from kivy.app import App
from kivy.lang.builder import Builder
from Domain.Slave import Slave
from Domain.Master import Master
from Domain.Project import Project
from Domain.Presentation import Presentation
from kivy.logger import Logger
from kivy.core.window import Window

"""
    HANDLES THE NAMING OF SLAVES AND MASTER AND THE MESSAGE SENT
    
    Called by Main.py. and uses GUICore.py to add the actual functionalities to the layouts,
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
        try:
            self.localip = IP.get_local_ip_address()
            self.connected = True
        except Exception as ex:
            self.connected = False
        self.localip = IP.get_local_ip_address()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        """
        Unbinds the keybindings made in __init__ and _on_keyboard_down
        :return: Nothing
        """
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """
        Defines keybindings to the program by overriding the _on_keyboard_down method. If you want to implement global
        key commands, it can be done here.
        :param keyboard:
        :param keycode:
        :param text:
        :param modifiers:
        :return:
        """
        if keycode[1] == 'b'and self.servicemode is not None:
            self.servicemode.layout.go_back()
        if keycode[1] == 'escape':
            App.stop(self)
        return True

    def build_config(self, config):
        """
        Sets default values for remu.ini confguration file
        and writes the file if it doesn't exist

        :param config:
        :return:
        """
        config.setdefaults('REMU', {
            'name': 'default',
            'start as slave': 'false',
            'tcp port': '8000',
            'udp port': '8555',
            'ftp port': '8005',
            'broadcast address': '<broadcast>'
        })

    def build(self):
        """
        The building method uses the GUI/remu.kv file that produces the look of the requested layouts
        and GUIFactory that adds the functionalities to those layouts.
        """
        self.config = self.load_config()['REMU']
        return BuildKV

    def on_start(self):
        """
        Starts the application in slave mode if the option is set in config file
        """
        if self.config.getboolean('start as slave'):
            self.root.add_slave_layout()


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
            empty_project = Project()

            # Uncomment to test
            # empty_project.create_test_presentation()
            new_master.setup_project(empty_project)
            new_master.load_project_to_gui()
        else:
            new_slave = Slave(layout)
            tcp_port = self.config.getint('tcp port')
            new_slave.set_master_connection(RemuTCP(new_slave, port=tcp_port))
            self.set_servicemode(new_slave, False)

    def end_presentation(self):
        """
        Ends the presentation by calling the current servicemode's end_presentation method.
        slave servicemode end_presentation not yet implemented
        """
        if self.isMaster:
            self.servicemode.end_presentation()

    def reset_servicemode(self):
        """
        Sets the service mode to none and resets the resources used by the service mode
        :return: Nothing
        """
        self.end_presentation()
        self.close_connections()
        self.servicemode = None

    def close_connections(self):
        """
        Closes all established connections and stops listening to any future connection attempts.
        """
        if self.servicemode:
            self.servicemode.close_all_connections()