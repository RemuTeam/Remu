from kivy.uix.screenmanager import ScreenManager, Screen
from Domain.PicPresentation import PicPresentation

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
    pass


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
    msg_sent = 0;

    """
    Increments the amount of clicks and returns the
    incremented value.
    """
    def increment(self):
        self.msg_sent += 1
        return str(self.msg_sent)


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
        self.pic_presentation = PicPresentation()

    """
    Handles the functionality of clicks in the Slave GUI.
    """
    def button_pressed(self):
        self.show_next()

    """
    Hides or shows other elements except the image element
    """
    def show_only_picture(self, show=False):
        if show:
            for child in self.children[0].children:
                print(str(child) + " / " + str(child.cls))
                if len(child.cls) > 0:
                    print("was true")
                    child.y = 6000
        else:
            for child in self.children[0].children:
                if len(child.cls) > 0:
                    child.y = 0


    """
    Shows the next element of the show
    """
    def show_next(self):
        next_pic_filename = self.pic_presentation.get_next()
        if next_pic_filename is not None:
            self.show_only_picture(True)
            self.ids.picture.source = next_pic_filename
            self.get_parent_window().fullscreen = True
        else:
            self.show_only_picture(False)
            self.ids.picture.source = ''
            self.get_parent_window().fullscreen = False

"""
Fullscreen layout for presenting content
"""
class PresentationLayout(Screen):
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
