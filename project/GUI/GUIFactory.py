from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from Domain.Slave import Slave
from Domain.Master import Master
from Domain.Command import Notification
from RemuTCP.RemuTCP import RemuTCP
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
        self.presentation = None
        self.master = Master(self)

    """
    Sets the address for GUI purposes, but does not control the actual connection
    """
    def set_address_to_gui(self, address):
        self.label_text = address

    def add_slave_connection(self, address):
        self.master.add_slave(address)

    def send_message_to_slave(self):
        self.master.request_next()

    """
    Increments the amount of clicks and returns the
    incremented value.
    """
    def increment(self):
        self.msg_sent += 1
        return str(self.msg_sent)

    """
    Opens the warning pop-up to master, asking if they are sure they want to go back
    """
    def show_master_back_popup(self):
        MasterBackPopUp().open()

    """
    Update the presentation information on the layout
    
    Not yet implemented
    """
    def update_presentation(self, data):
        pass

    """
    Update the presentation status on the layout
    """
    def update_presentation_status(self, data):
        self.msg_sent_amount.text = str(data)

    def update_connection(self, data):
        self.set_address_to_gui(str(data))

    """
    Handles the received notification from master
    
    notification:   a Notification enum
    data:           an object
    """
    def notify(self, notification, data):
        return self.messagehandler[notification](self, data)

    """
    A dictionary of Notification-Function pairs for the purpose of
    updating the layout on predefined events.
    """
    messagehandler = {Notification.PRESENTATION_UPDATE: update_presentation,
                      Notification.PRESENTATION_STATUS_CHANGE: update_presentation_status,
                      Notification.CONNECTION_FAILED: update_connection,
                      Notification.CONNECTION_ESTABLISHED: update_connection}


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
        self.slave = None

    def on_enter(self, *args):
        if self.slave is None:
            self.slave = Slave(self)
            self.connection = RemuTCP(self.slave)

    """
    Sets the app's main window to full screen and hides the
    mouse cursor.
    """
    def prepare_for_presentation_mode(self):
        window = self.get_root_window()
        self.parent.get_screen('presentation_layout').set_slave(self.slave)
        window.show_cursor = False
    """
     Opens the warning pop-up to slave, asking if they are sure they want to go back
    """
    def show_slave_back_popup(self):
        SlaveBackPopUp().open()


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

    def button_pressed(self):
        self.show_next()

    def on_enter(self, *args):
        self.slave.set_layout(self)
        self.slave.presentation.get_filenames()

    def set_slave(self, slave):
        self.slave = slave

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

"""
These represent the popups that take the maste or slave back to the switch layout if they decide to 
break the connection
"""
class MasterBackPopUp(Popup):
    pass
class SlaveBackPopUp(Popup):
    pass

"""
SlavePresentation is the visual presentation of the slave in the master view. It contains information about the slave's
state and visuals associated with it
"""
class SlavePresentation(BoxLayout):
    pass

"""
SlaveVisualProperty is the class of the slave's visuals. It represents a single visual property of the slave's properties
"""
class SlaveVisualProperty(Button):

    visual_name = StringProperty('')

    #def __init__(self, image_source):
    #    self.visual_name = image_source

    def on_press(self):
        print("Showing visual property information")

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
