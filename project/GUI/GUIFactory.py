# coding: latin-1

from kivy.uix.screenmanager import ScreenManager, Screen


class SwitchLayout(Screen):

    def master_button_pressed(self):
        self.gui_factory.remuapp.set_master()
        self.gui_factory.remuapp.add_slave("192.168.1.1")

    def slave_button_pressed(self):
        self.gui_factory.remuapp.set_slave()


class MasterGUILayout(Screen):
    msg_sent = 0;

    def increment(self):
        self.msg_sent += 1
        return str(self.msg_sent)


class SlaveGUILayout(Screen):
    def __init__(self, **kwargs):
        super(SlaveGUILayout, self).__init__(**kwargs)

    def button_pressed(self):
        self.source = ''

    def button_released(self):
        self.source = 'a.jpg'


class ScreenManager(ScreenManager):
    pass


class GUIFactory:
    """GUIFactory määrittelee käyttöliittymän komponenttien toiminnallisuuden (= määrittelee metodit)
       Main kutsuu GUIFactorya tarvittaessa, jolloin GUIFactory luo komponentit ja lataa ulkoasun remu.kv -tiedostosta"""
    remuapp = None

    def __init__(self):
        pass

    def set_parent(self, remuapp):
        self.remuapp = remuapp
