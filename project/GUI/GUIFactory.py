from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class GUIFactory:
    def __init__(self):
        pass

    def hello(self):
        print("Hello")

    def getMasterSwitchGUI(self):
        return MasterSwitchLayout()
        #if isMaster:
        #    return MasterGUI()
        #else:
        #    return SlaveGUI()



class MasterSwitchLayout(BoxLayout):

    pass


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
