from kivy.uix.popup import Popup
from kivy.event import EventDispatcher

from GUI.CustomWidgets import CheckBoxBonanza
from kivy.app import App

class BindPresentationToSlavePopUp(Popup, EventDispatcher):
    """
    A kivy popup that allows the user to remove made presentations in master mode
    """

    def __init__(self, available_slaves, presentation, master, button):
        super(BindPresentationToSlavePopUp, self).__init__()
        self.checkboxes = []
        self.populate_presentation_list(available_slaves)
        self.presentation = presentation
        self.listener = master
        self.selected_slave = None
        self.button = button

    def populate_presentation_list(self, available_slaves):
        """
        adds the checkboxlist and corresponding presentation list to RemovePresentationPopUp
        :param available_slaves:
        :return:
        """
        slave_list = self.ids.slave_connection_list
        for p in available_slaves:
            cbb = CheckBoxBonanza(p, 0.05, self.on_checkbox_active)
            cbb.ids.checker.group = "check yo self before you wreck yo self"
            self.checkboxes.append(cbb)
            slave_list.add_widget(cbb)

    def on_checkbox_active(self, checkbox, value):
        """
        checks if the presentation's box has been checked or not
        :param checkbox:
        :param value:
        :return:
        """
        if value:
            self.selected_slave = checkbox.label

    def confirm(self):
        if self.selected_slave:
            slave = App.get_running_app().servicemode.slave_connections[self.selected_slave]
            self.listener.bind_slave_to_presentation(self.presentation, self.selected_slave)
            self.button.slave_connection = slave
            self.button.text = self.button.text.split("\n")[0] + "\n" + self.selected_slave
            self.button.background_color = (1, 1, 1, 1)
