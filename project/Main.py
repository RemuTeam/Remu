import kivy

from project.GUI.GUIFactory import GUIFactory
from kivy.app import App

kivy.require('1.1.0')


class MyApp(App):

    guimaker = GUIFactory()
    isMaster = False

    def build(self):
        return self.guimaker.getGUI(self.isMaster)


if __name__ == '__main__':
    MyApp().run()
