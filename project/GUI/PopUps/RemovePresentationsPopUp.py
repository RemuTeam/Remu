from kivy.uix.popup import Popup
from kivy.event import EventDispatcher

from GUI.CustomWidgets import CheckBoxBonanza

class RemovePresentationsPopUp(Popup, EventDispatcher):
    """
    A kivy popup that allows the user to remove made presentations in master mode
    """

    def __init__(self, presentations, listener):

        super(RemovePresentationsPopUp, self).__init__()
        self.checkboxes = []
        self.populate_presentation_list(presentations)
        self.selected_presentations = []
        self.listener = listener

    def populate_presentation_list(self, presentations):
        """
        adds the checkboslist and corresponding presentation list to RemovePresentationPopUp
        :param presentations:
        :return:
        """
        presentation_list = self.ids.presentation_list
        for p in presentations:
            cbb = CheckBoxBonanza(p, 0.05, self.on_checkbox_active)
            presentation_list.add_widget(cbb)
            self.checkboxes.append(cbb)

    def on_checkbox_active(self, checkbox, value):
        """
        checks if the presentation's box has been checked or not
        :param checkbox:
        :param value:
        :return:
        """
        if value:
            self.selected_presentations.append(checkbox.label)
        else:
            self.selected_presentations.remove(checkbox.label)

    def inform_listener(self):
        """
        informs master_layout of the selected presentations that are to be removed
        :return:
        """
        self.listener.notify_remove_presentations(self.selected_presentations)