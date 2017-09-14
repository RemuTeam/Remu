# coding: latin-1

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class GUIFactory:
    """GUIFactory määrittelee käyttöliittymän komponenttien toiminnallisuuden (= määrittelee metodit)
       Main kutsuu GUIFactorya tarvittaessa, jolloin GUIFactory luo komponentit ja lataa ulkoasun remu.kv -tiedostosta"""
    def __init__(self):
        pass

    def hello(self):
        print("Hello")

    def getMasterSwitchLayout(self):
        return MasterSwitchLayout()

    def getMasterGUILayout(self):
        return MasterGUILayout()

class MasterGUILayout(BoxLayout):

    def send_message_to_slave(self):
        amount = int(self.messages_sent.text)
        self.messages_sent.text = str(amount + 1)

class MasterSwitchLayout(BoxLayout):

    def hello(self):
        print("Hello")


class MasterGUI(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MasterGUI, self).__init__(**kwargs)

    def on_press(self):
        self.source = 'a.jpg'

    def on_release(self):

        self.source = ''


class SlaveGUI(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(SlaveGUI, self).__init__(**kwargs)

    def on_press(self):
        self.source = ''

    def on_release(self):
        self.source = 'a.jpg'
