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

    