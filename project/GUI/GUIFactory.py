# coding: latin-1

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen


class SwitchLayout(Screen):
    pass


class MasterGUILayout(Screen):
    msg_sent = 0;


    def increment(self):
        self.msg_sent += 1
        return str(self.msg_sent)


class SlaveGUI(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(SlaveGUI, self).__init__(**kwargs)

    def on_press(self):
        self.source = ''

    def on_release(self):
        self.source = 'a.jpg'


class ScreenManager(ScreenManager):
    pass


class GUIFactory:
    """GUIFactory määrittelee käyttöliittymän komponenttien toiminnallisuuden (= määrittelee metodit)
       Main kutsuu GUIFactorya tarvittaessa, jolloin GUIFactory luo komponentit ja lataa ulkoasun remu.kv -tiedostosta"""

    def __init__(self):
        pass