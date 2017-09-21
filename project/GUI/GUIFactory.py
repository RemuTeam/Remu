from kivy.uix.screenmanager import ScreenManager, Screen


"""
Produces the GUI-layout that allows the user to choose
between Master- and Slave-mode.
"""
class SwitchLayout(Screen):
    pass


"""
Produces the Master-mode's GUI-layout that allows the
user to communicate with Slave-devices.
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
"""
class SlaveGUILayout(Screen):

    def __init__(self, **kwargs):
        super(SlaveGUILayout, self).__init__(**kwargs)
        self.showpic = False

    def button_pressed(self):
        self.showpic = not self.showpic
        if self.showpic:
            self.ids.picture.source = 'a.jpg'
        else:
            self.ids.picture.source = ''


class ScreenManager(ScreenManager):
    pass


"""
GUIFactory maarittelee kayttaliittyman komponenttien toiminnallisuuden (= maarittelee metodit)
Main kutsuu GUIFactorya tarvittaessa, jolloin GUIFactory luo komponentit ja lataa ulkoasun remu.kv -tiedostosta
"""
class GUIFactory:
    remuapp = None

    def __init__(self):
        pass

    def set_parent(self, remuapp):
        self.remuapp = remuapp
