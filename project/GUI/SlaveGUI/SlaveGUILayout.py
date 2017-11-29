from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
from GUI.PopUps.PopUps import SlaveBackPopUp

class SlaveGUILayout(Screen):
    """
    Produces the Slave-mode's GUI-layout that reacts to
    the Master-devices commands.

    Inherits kivy.uix.screenmanager.Screen
    """

    # layout uses this StringProperty to show current service mode
    info_text = StringProperty('Currently in slave mode')

    def __init__(self, **kwargs):
        """
        In the constructor the class and instance are passed
        to the superclass' __init__ function
        """
        super(SlaveGUILayout, self).__init__(**kwargs)
        self.slave = None

    def on_pre_enter(self, *args):
        if self.slave is None:
            self.slave = App.get_running_app().get_slave(self)
            self.slave.set_layout(self)

    def init_presentation(self):
        self.prepare_for_presentation_mode()

    def prepare_for_presentation_mode(self):
        """
        Sets the app's main window to full screen and hides the
        mouse cursor.
        """
        window = self.get_root_window()
        window.show_cursor = False
        App.get_running_app().root.change_screen_to("presentation_layout")

    def show_slave_back_popup(self):
        """
        Opens the warning pop-up to slave, asking if they are sure they want to go back
        """
        SlaveBackPopUp().open()

    def set_info_text(self, info_text):
        self.info_text = info_text
