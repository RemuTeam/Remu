from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
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
    Handles the functionality of clicks in the Slave GUI.
    """
    def button_pressed(self):
        self.showpic = not self.showpic
        if self.showpic:
            self.ids.picture.source = 'a.jpg'
        else:
            self.ids.picture.source = ''

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
