from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class CheckBoxBonanza(BoxLayout):
    """
    A kivy widget class to hold a Checkbox and a Label
    """
    presentation_name = StringProperty('')

    def __init__(self, presentation_name, size_hint_y, callback):
        """
        Constructor function

        :param presentation_name: a string, the presentation's name
        :param size_hint_y: a floating-point number x, where 0 < x <= 1,
                defines the proportion the element occupies of the layout's height
        :param callback: the callback function to call when a checkbox is checked
        """
        super(CheckBoxBonanza, self).__init__()
        self.presentation_name = presentation_name
        self.size_hint_y = size_hint_y
        self.ids.checker.bind(active=callback)
