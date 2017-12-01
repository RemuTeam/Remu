from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.popup import Popup

from GUI.CustomWidgets import CheckBoxBonanza


class FileHandlerPopUp(Popup, EventDispatcher):
    """
    A file selection and handling popup superclass

    Opens a PopUp for the user to choose file / files
    """
    default_path = StringProperty('')
    button_text = StringProperty('')
    multiselect = BooleanProperty()
    title = StringProperty('')
    filters = ListProperty()
    local_presentation_selection = ListProperty()

    def __init__(self, title, default_path, callback, callback_button_text, filters=[], imported_files=None,
                 selected_presentations=None, multiselect=False, presentation_names=None, test_mode=False):
        """
        A constructor
        :param title: a string, the title to show in the popup
        :param imported_files: the list to populate with selected files
        :param default_path: a string, the default path to open the filechooser
        :param callback: the function to call when the callback_button is pressed
        :param callback_button_text: a string the text to display in the button that invokes the callback function
        :param filters: a list of strings, filters the files to show, refer to kivy.uix.filechooser docs, no filters by default
        :param selected_presentations: the list to populate with the selected presentations, None by default
        :param multiselect: a boolean, True if allowed to select multiple files, False by default
        :param presentation_names: a list of strings, the names of the presentations opened in gui, None by default
        :param test_mode: a boolean; if True, some functionality is skipped, False by default
        """
        super(FileHandlerPopUp, self).__init__()
        self.filters = filters
        self.imported_files = imported_files
        self.exit_callback = callback
        if presentation_names is not None:
            self.populate_presentation_list(presentation_names)
        self.selected_presentations = selected_presentations
        self.ids.filechooser.bind(selection=self.check_selections)
        if self.selected_presentations is not None:
            self.bind(local_presentation_selection=self.check_selections)
        self.default_path = default_path
        self.test_mode = test_mode
        self.title = title
        self.multiselect = multiselect
        self.button_text = callback_button_text

    def on_dismiss(self):
        self.ids.filechooser.unbind(selection=self.check_selections)
        if self.selected_presentations is not None:
            self.unbind(local_presentation_selection=self.check_selections)

    def check_selections(self, instance, value):
        selection = self.ids.filechooser.selection
        callback_button = self.ids.callback_button
        if len(selection) == 0 or \
                (self.selected_presentations is not None and len(self.selected_presentations) == 0):
            callback_button.disabled = True
        else:
            callback_button.disabled = False

    def populate_presentation_list(self, presentations):
        presentation_list = self.ids.presentation_list
        for p in presentations:
            presentation_list.add_widget(CheckBoxBonanza(p, 0.05, self.on_checkbox_active))

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.selected_presentations.append(checkbox.label)
            if self.local_presentation_selection is not None:
                self.local_presentation_selection.append(checkbox.label)
        else:
            self.selected_presentations.remove(checkbox.label)
            if self.local_presentation_selection is not None:
                self.local_presentation_selection.remove(checkbox.label)
