import kivy
kivy.require('1.1.0')

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

class MyButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)

    def on_press(self):
        self.source = 'a.jpg'

    def on_release(self):

        self.source = ''


class MyApp(App):

    def build(self):
        return MyButton()


if __name__ == '__main__':
    MyApp().run()