from kivy.properties import StringProperty
from kivy.uix.popup import Popup

"""
MasterBackPopUp and SlaveBackPopUp classes represent the popups that take the master or slave back to the switch layout 
if they decide to break the connection
"""


class MasterBackPopUp(Popup):
    pass


class SlaveBackPopUp(Popup):
    pass


class ExceptionAlertPopUp(Popup):
    error_msg = StringProperty('')
    error_title = StringProperty('')

    def __init__(self, title, exception):
        super(ExceptionAlertPopUp, self).__init__()
        self.error_title = title
        self.error_msg = exception.__class__.__name__ + ": " + str(exception)