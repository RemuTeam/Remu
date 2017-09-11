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

    def getGUI(self, isMaster):
        return MenuGUI()
        #if isMaster:
        #    return MasterGUI()
        #else:
        #    return SlaveGUI()



class MenuGUI(BoxLayout):

    def __init__(self):
        super(MenuGUI, self).__init__()
        self.orientation = 'vertical'

        self.add_widget(Label(text="Master vai slave?"))

        box_layout = BoxLayout()
        box_layout.add_widget(Button(text="Master"))
        box_layout.add_widget(Button(text="Slave"))

        self.add_widget(box_layout)


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
