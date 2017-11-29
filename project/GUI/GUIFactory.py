from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from GUI.MasterGUI.MasterGUILayout import MasterGUILayout
from GUI.MasterGUI.ProjectOverview import ProjectOverview  # Do not remove, needed by RemuSM!
from GUI.SlaveGUI.PresentationLayout import PresentationLayout
from GUI.SlaveGUI.SlaveGUILayout import SlaveGUILayout
from GUI.PopUps.PopUps import ExceptionAlertPopUp

"""
CLASS LIBRARY TO HANDLE THE FUNCTIONALITY OF GUI LAYOUTS

The layouts' components, administrative information (such as
ids and names) and functions to perform on triggered events
are defined in the layout file:

project/GUI/remu.kv
"""



class SwitchLayout(Screen):
    """
    Produces the GUI-layout that allows the user to choose
    between Master- and Slave-mode.

    Inherits kivy.uix.screenmanager.Screen
    """
    text = StringProperty('')

    def goto_master_mode(self):
        """
        Setups the app to be used in the master mode
        :return: ExceptionAlertPopup if adding master not possible
        """
        app = App.get_running_app()
        try:
            app.root.add_master_layout()
        except Exception as ex:
            app.reset_servicemode()
            app.root.rm_master_layout()
            ExceptionAlertPopUp("Error going to master mode:", ex).open()


    def add_address(self, address):
        self.text = address


class InfoLayout(Screen):
    with open('infotext.txt') as f:
        t = f.read()
    text = t


class RemuSM(ScreenManager):
    """
    Handles changing the GUI-layouts as different screens for the
    application, and also acts as the root widget

    Inherits kivy.uix.screenmanager.ScreenManager
    """

    def __init__(self, **kwargs):
        """
        Initializes references to differents screens as 'None'
        """
        super(RemuSM, self).__init__(**kwargs)
        self.master_screen = None
        self.slave_screen = None
        self.presentation_screen = None
        self.info_screen = None

    def add_master_layout(self):
        """
        Creates a new master layout, and sets it to be the current screen
        """

        if self.master_screen is None:
            self.master_screen = MasterGUILayout(name='master_gui_layout')
            self.add_widget(self.master_screen)
        self.current = 'master_gui_layout'

    def add_slave_layout(self):
        """
        Creates a new slave layout and a presentation layout, and sets the slave layout
        to be the current screen
        """
        if self.slave_screen is None:
            self.slave_screen = SlaveGUILayout(name='slave_gui_layout')
            self.presentation_screen = PresentationLayout(name='presentation_layout')
            self.add_widget(self.slave_screen)
            self.add_widget(self.presentation_screen)
        self.current = 'slave_gui_layout'

    def add_info_layout(self):
        if self.info_screen is None:
            self.info_screen = InfoLayout(name='info_gui_layout')
            self.add_widget(self.info_screen)
        self.current = 'info_gui_layout'

    def change_screen_to(self, name):
        """
        Changes the screen according to the screen name parameter
        """
        self.current = name

    def rm_master_layout(self):
        """
        Removes the master layout from screenmanager's screens
        """
        #self.remove_widget(self.master_screen)
        self.master_screen=None
        self.change_screen_to("switch_layout")

    def rm_slave_layout(self):
        """
        Removes the slave layout and the presentation layout from screenmanager's screens
        """
        self.remove_widget(self.slave_screen)
        self.remove_widget(self.presentation_screen)
        self.slave_screen=None
        self.presentation_screen=None
        self.change_screen_to("switch_layout")

    def get_current_layout(self):
        return self.current_screen


class GUIFactory:
    """
    GUIFactory defines the functions for the layout components
    The current running app is set as the GUIFactory instance's
    parent in Main.py
    """
    remuapp = None

    def __init__(self):
        pass

    def set_parent(self, remuapp):
        """
        Sets the current running app as the GUIFactory instance's
        parent
        """
        self.remuapp = remuapp