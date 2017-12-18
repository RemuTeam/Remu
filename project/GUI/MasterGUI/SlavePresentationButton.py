from kivy.uix.button import Button

class SlavePresentationButton(Button):

    def __init__(self, **kwargs):
        super(SlavePresentationButton, self).__init__(**kwargs)
        self.slave_connection = None