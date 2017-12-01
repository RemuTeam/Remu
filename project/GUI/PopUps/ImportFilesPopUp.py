import os
from shutil import copyfile

from Constants.TestReturnValue import *
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ListProperty
from kivy.uix.popup import Popup

from Constants.SupportedFileTypes import AllSupportedFormats
from GUI.CustomWidgets import CheckBoxBonanza
from GUI.PopUps.FileSavingDialogPopUp import FileSavingDialogPopUp


class ImportFilesPopUp(Popup, EventDispatcher):
    """
    A file selection and opening popup
    """
    media_path = StringProperty('')
    supportedFormats = ListProperty([])
    local_presentation_selection = ListProperty([])

    def __init__(self, listener, imported_files, presentations,
                 selected_presentations, media_path, test_mode=False):
        """
        Constructor

        :param listener: the component to inform about file imports
        :param imported_files: a kivy ListProperty to store files that are imported
        :param presentations: a list of Presentation names
        :param
        """
        super(ImportFilesPopUp, self).__init__()
        self.supportedFormats = AllSupportedFormats
        self.imported_files = imported_files
        self.listener = listener
        self.populate_presentation_list(presentations)
        self.selected_presentations = selected_presentations
        self.ids.filechooser.bind(selection=self.check_selections)
        self.bind(local_presentation_selection=self.check_selections)
        self.media_path = media_path
        self.test_mode = test_mode

    def on_dismiss(self):
        self.ids.filechooser.unbind(selection=self.check_selections)
        self.unbind(local_presentation_selection=self.check_selections)

    def check_selections(self, instance, value):
        selection = self.ids.filechooser.selection
        import_button = self.ids.import_button
        if len(selection) == 0 or len(self.selected_presentations) == 0:
            import_button.disabled = True
        else:
            import_button.disabled = False

    def populate_presentation_list(self, presentations):
        presentation_list = self.ids.presentation_list
        for p in presentations:
            presentation_list.add_widget(CheckBoxBonanza(p, 0.05, self.on_checkbox_active))

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.selected_presentations.append(checkbox.label)
            self.local_presentation_selection.append(checkbox.label)
        else:
            self.selected_presentations.remove(checkbox.label)
            self.local_presentation_selection.remove(checkbox.label)


    def import_files_for_presentation(self, path, selection):
        """
        Opens one or multiple files from a path
        :param path: the path to open files from
        :param selection: a list the selected files in the path
        :param presentation: the presentation to open the files to
        :return: None
        """
        self.listener.import_started(len(selection))
        if not self.test_mode:
            self.import_files_from_media_folder(path, selection, self.listener)

    def import_files_from_media_folder(self, path, selected_files, listener):
        """
        Get the selected files from media folder.
        If the file doesn't exists in the media folder,
        it will be copied there first.

        :param path: the path of the files to import from
        :param selected_files: the files selected from some path
        :param callback: the function to call when importation is ready
        :return: a list of files copied to media folder
        """
        for filee in selected_files:
            separated_paths = filee.split(os.sep)
            file_to_write = os.path.join(self.media_path, separated_paths[len(separated_paths) - 1])
            self.copy_file(path, filee, file_to_write, self.imported_files, listener)

    def copy_file(self, path, source, destination, filename_list, listener):
        """
        Copies the source file as the destination file
        and returns the file with complete path.
        If the destination file exists, it will not be
        overwritten.

        :param path: the path of the files to import from
        :param source: a string, the source file with path
        :param destination: a string, the derstination file with path
        :param filename_list: the list to append the created filename
        :return: the destination file
        """
        if path != self.media_path and os.path.isfile(destination):
            if self.test_mode:
                return TestReturnValue.FileSavingDialogPopUp
            FileSavingDialogPopUp(source, destination, filename_list, listener, self.media_path).open()
        elif path != self.media_path:
            copyfile(source, destination)
            filename_list.append(destination)
            listener.notify_file_import()
        else:
            filename_list.append(destination)
            listener.notify_file_import()