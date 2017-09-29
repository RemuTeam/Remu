from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from Domain.Slave import Slave
from kivy.app import App

"""
CLASS LIBRARY TO HANDLE THE FUNCTIONALITY OF GUI LAYOUTS

The layouts' components, administrative information (such as
ids and names) and functions to perform on triggered events
are defined in the layout file:

project/GUI/remu.kv
"""

"""
Produces the GUI-layout that allows the user to choose
between Master- and Slave-mode.

Inherits kivy.uix.screenmanager.Screen
"""
class SwitchLayout(Screen):
    text = StringProperty('')

    def add_address(self, address):
        self.text = address


"""
Produces the Master-mode's GUI-layout that allows the
user to communicate with Slave-devices.

Inherits kivy.uix.screenmanager.Screen
"""
class MasterGUILayout(Screen):

    """
    A variable for debugging purposes to track the amount
    of clicks in the GUI
    """
    msg_sent = 0
    label_text = StringProperty('')

    def __init__(self, **kwargs):
        super(MasterGUILayout, self).__init__(**kwargs)


    def set_address(self, address):
        self.label_text = address

    """
    Increments the amount of clicks and returns the
    incremented value.
    """
    def increment(self):
        self.msg_sent += 1
        return str(self.msg_sent)
    def show_popup(self):
        Popp().open()


"""
Produces the Slave-mode's GUI-layout that reacts to
the Master-devices commands.

Inherits kivy.uix.screenmanager.Screen
"""
class SlaveGUILayout(Screen):

    """
    In the constructor the class and instance are passed
    to the superclass' __init__ function
    """
    def __init__(self, **kwargs):
        super(SlaveGUILayout, self).__init__(**kwargs)
        self.showpic = False

    """
    Sets the app's main window to full screen and hides the
    mouse cursor.
    """
    def prepare_for_presentation_mode(self):
        window = self.get_root_window()

        window.show_cursor = False


"""
Fullscreen layout for presenting content
"""
class PresentationLayout(Screen):
    """
    In the constructor the class and instance are passed
    to the superclass' __init__ function
    """
    def __init__(self, **kwargs):
        super(PresentationLayout, self).__init__(**kwargs)
        self.showpic = False
        self.slave = Slave()
        self.slave.presentation.get_filenames()

    def button_pressed(self):
        self.show_next()

    """
    Shows the next element of the show
    """
    def show_next(self):
        next_pic_filename = self.slave.presentation.get_next()
        if next_pic_filename is not None:
            self.ids.picture.source = next_pic_filename
        else:
            self.ids.picture.source = ''
            self.get_root_window().show_cursor = True
            self.slave.presentation.reset()
            App.get_running_app().root.current = "slave_gui_layout"

class Popp(Popup):
    pass
"""
Provides the GUI-layouts as different screens for the 
Kivy-layout file.

Inherits kivy.uix.screenmanager.ScreenManager
"""
class ScreenManager(ScreenManager):
    pass


"""
GUIFactory defines the functions for the layout components
The current running app is set as the GUIFactory instance's 
parent in Main.py
"""
class GUIFactory:
    remuapp = None

    """
    Empty constructor
    """
    def __init__(self):
        pass

    """
    Sets the current running app as the GUIFactory instance's
    parent
    """
    def set_parent(self, remuapp):
        self.remuapp = remuapp
