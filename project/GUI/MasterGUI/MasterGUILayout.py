from Constants.PathConstants import PathConstants
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger

from Constants.Command import Notification
from GUI.PopUps.ImportFilesPopUp import ImportFilesPopUp
from GUI.PopUps.PopUps import MasterBackPopUp
from GUI.PopUps.RemovePresentationsPopUp import RemovePresentationsPopUp
from GUI.PopUps.PopUps import ExceptionAlertPopUp
from GUI.PopUps.ProjectOpenPopUp import ProjectOpenPopUp
from GUI.PopUps.ProjectSavePopUp import ProjectSavePopUp

class MasterGUILayout(Screen, EventDispatcher):
    """
    Produces the Master-mode's GUI-layout that allows the
    user to communicate with Slave-devices.

    Inherits kivy.uix.screenmanager.Screen
    """

    presenting_disabled = BooleanProperty(True)
    debug_text = StringProperty('Use this text space for debug')

    """
    The import counter is used to keep track on imported files on a
    single importation event.

    Values and their effects:
    -1      Handled as "the counter is reset and no imports are incomplete".
     0      The import is complete, the list of imported files is up to date.
            The list of files should be processed and the counter reset.
    1...n   The amount of files still to be imported.
    """
    import_counter = NumericProperty()
    import_list = ListProperty()
    import_to_presentations = ListProperty()

    def __init__(self, **kwargs):
        super(MasterGUILayout, self).__init__(**kwargs)
        self.presentation = None
        self.start_pres_btn = self.ids.start_pres
        self.back_btn = self.ids.back_button
        self.show_next_btn = self.ids.show_next
        self.stop_pres_btn = self.ids.stop_pres
        self.change_visibility_of_multiple_elements([self.show_next_btn, self.stop_pres_btn], True)
        self.bind(import_counter=self.import_counter_update)
        self.reset_import_counter()
        self.import_list = []
        self.import_to_presentations = []
        self.project_overview = self.ids.project_overview
        self.master = None

    def go_back(self):
        Logger.warning("MasterGUILayout: Back method not implemented")

    def setup_project(self, project):
        self.project_overview.project = project

    def notify_file_import(self):
        """
        Notifies the layout for a single file import
        :return: None
        """
        self.import_counter -= 1

    def reset_import_counter(self):
        """
        Resets the import counter.
        :return: None
        """
        self.import_counter = -1

    def import_started(self, value):
        """
        Updates the import counter's value.
        :param value: an integer, the new value
        :return: None
        """
        self.import_counter = value

    def import_counter_update(self, instance, value):
        """
        A callback function to call when the import counter's value changes.
        :return: None
        """
        if value == 0:
            for presentation_name in self.import_to_presentations:
                self.project_overview.add_files_to_a_presentation(presentation_name, self.import_list)
            self.__clear_lists(self.import_list, self.import_to_presentations)
            self.reset_import_counter()

    @staticmethod
    def __clear_lists(*lists):
        """
        Delete the contents of the lists given as parameter
        :param lists: the lists to empty
        :return: None
        """
        for list in lists:
            del list[:]

    def on_pre_enter(self):
        """
        An inherited maintenance function
        Called when the switch to this Screen has started
        :return: None
        """
        self.master = App.get_running_app().get_master(self)

    def check_text(self, text):
        """
        A callback function to call when the bound TextProperty's
        text changes.
        :param text: a string, the content of the StringProperty's text
        :return:
        """
        self.ids.new_presentation_button.disabled = not text

    def add_slave_connection(self, address):
        """
        Adds a new slave
        :param address: a string, the slave's address to add
        :return:
        """
        self.master.add_slave(address)

    def create_new_presentation(self, name, presentation=None):
        """
        Creates a new presentation into the master's gui
        :param name: Name of the presentation to be created
        :return: Nothing
        """
        self.project_overview.new_presentation_to_overview(name, presentation)
        self.ids.txt_input.text = ""

    def request_next_element_from_all_slaves(self):
        """
        Requests the next visual element from all slaves
        :return: Nothing
        """
        self.master.request_next()

    def start_presentation(self):
        """
        Changes the master's editor mode to the presentation mode. It hides the editor mode buttons and shows the
        presentation mode buttons, and sends the presentations the user has made to the slaves
        :return: Nothing
        """
        try:
            self.master.send_presentations_to_slaves()
            self.change_visibility_of_multiple_elements([self.start_pres_btn, self.back_btn], True)
            self.change_visibility_of_multiple_elements([self.show_next_btn, self.stop_pres_btn], False)
            self.project_overview.disable_rearrangement_of_buttons()
        except Exception as ex:
            ExceptionAlertPopUp("Error sending presentations to slave devices", ex).open()

    def stop_presentation(self):
        """
        Changes the editor mode into presentation mode. This method should lock the presentation
        :return:
        """
        self.change_visibility_of_multiple_elements([self.show_next_btn, self.stop_pres_btn], True)
        self.change_visibility_of_multiple_elements([self.start_pres_btn, self.back_btn], False)
        self.master.end_presentation()
        self.project_overview.reset_all_presentations()

    def change_visibility_of_multiple_elements(self, list, hide):
        """
        Uses the hide_widget and show widget to change visibility of multiple elements with a single method call
        :param list: Widgets that are hidden or shown
        :param hide: Boolean, true if you want to hide the widget
        :return: Nothing
        """
        for element in list:
            if hide:
                self.hide_widget(element)
            else:
                self.show_widget(element)

    def hide_widget(self, widget):
        """
        Hides the widget. Duhh.
        :param widget: Widget to be hidden
        :return: Nothing
        """
        widget.opacity = 0
        widget.size_hint_y = 0
        widget.size_hint_x = 0
        widget.width = '0dp'

    def show_widget(self, widget):
        """
        See the method above
        :param widget: Widget to be shown
        :return: Nothing
        """
        widget.opacity = 1
        widget.size_hint_y = 1
        widget.size_hint_x = 1

    def show_master_back_popup(self):
        """
        Opens the warning pop-up to master, asking if they are sure they want to go back
        """
        MasterBackPopUp().open()

    def show_remove_presentations_popup(self):
        """
        Opens the popup that allows master to remove presentations
        """
        RemovePresentationsPopUp(self.get_presentation_list(), self).open()

    def get_presentation_list(self):
        """
        Get all the names of presentations from project overview
        :return: a list of string, the names of presentations
        """
        presentation_names = []
        for key, value in self.project_overview.slave_presentations.items():
            presentation_names.append(key)
        return  presentation_names

    def show_open_file_popup(self):
        """
        Opens a Filechooser to load files
        :return: None
        """
        ImportFilesPopUp(self, self.import_list, self.get_presentation_list(), self.import_to_presentations,
                         PathConstants.ABSOLUTE_MEDIA_FOLDER).open()

    def generate_presentation(self, slave_connection):
        """
        Generate the presentation information on the layout on connection to a slave.
        """
        self.project_overview.update_slave_to_overview(slave_connection)

    def remove_slave_presentation(self, data):
        """
        Remove possibly existing SlavePresentation widget based on the
        SlaveConnection object
        """
        self.project_overview.remove_slave_from_overview(data.full_address)

    def update_presentation_status(self, data=None):
        """
        Update the presentation status on the layout
        """
        self.project_overview.update_presentation_state()

    def update_connection_to_gui(self, slave_connection):
        """
        If the slave connection is lost, notifies the project.
        """
        if not slave_connection.connected:
            self.project_overview.notify_connection_lost(slave_connection)


    def start_presentation_button_disabled(self, is_disabled):
        """
        Enables the start_pres button, enabling starting of the presentation.
        :param is_disabled: a boolean; if True, presenting is disabled, otherwise enabled
        :return: Nothing
        """
        self.presenting_disabled = is_disabled

    def notify_remove_presentations(self, selected_presentations):
        """
        Remove_presentation popup calls this method to infrom master what presentations
        were selected to be removed
        :param selected_presentations: a list, the presentations to be removed
        :return:
        """
        for name in selected_presentations:
            self.project_overview.remove_presentation(name)

    def clear_presentations(self):
        self.project_overview.remove_presentations()

    def notify(self, notification, data=None):
        """
        Handles the received notification from master

        notification:   a Notification enum
        data:           an object
        """
        return self.messagehandler[notification](self, data)

    """
    A dictionary of Notification-Function pairs for the purpose of
    updating the layout on predefined events.
    """
    messagehandler = {Notification.PRESENTATION_UPDATE: generate_presentation,
                      Notification.PRESENTATION_STATUS_CHANGE: update_presentation_status,
                      Notification.CONNECTION_FAILED: update_connection_to_gui,
                      Notification.CONNECTION_ESTABLISHED: update_connection_to_gui,
                      Notification.CONNECTION_TERMINATED: remove_slave_presentation,
                      Notification.PRESENTING_DISABLED: start_presentation_button_disabled
                      }

    def error(self, message, exception):
        ExceptionAlertPopUp(message, exception).open()


class BottomPanel(BoxLayout):
    def open_project(self):
        ProjectOpenPopUp(App.get_running_app().servicemode, PathConstants.ABSOLUTE_PROJECT_FOLDER).open()

    def save_project(self):
        ProjectSavePopUp(App.get_running_app().servicemode, PathConstants.ABSOLUTE_PROJECT_FOLDER).open()