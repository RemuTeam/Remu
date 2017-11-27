from kivy.uix.popup import Popup
import os
from shutil import copy
from shutil import copyfile

from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from Domain.SupportedFileTypes import AllSupportedFormats
from Domain.TestReturnValue import TestReturnValue

"""
MasterBackPopUp and SlaveBackPopUp classes represent the popups that take the master or slave back to the switch layout 
if they decide to break the connection
"""


class MasterBackPopUp(Popup):
    pass


class SlaveBackPopUp(Popup):
    pass


class BindPresentationToSlavePopUp(Popup, EventDispatcher):
    """
    A kivy popup that allows the user to remove made presentations in master mode
    """

    def __init__(self, available_slaves, presentation, listener, button):
        super(BindPresentationToSlavePopUp, self).__init__()
        self.populate_presentation_list(available_slaves)
        self.presentation = presentation
        self.listener=listener
        self.selected_slave = None
        self.button = button

    def populate_presentation_list(self, available_slaves):
        """
        adds the checkboslist and corresponding presentation list to RemovePresentationPopUp
        :param available_slaves:
        :return:
        """
        slave_list = self.ids.slave_connection_list
        for p in available_slaves:
            cbb = CheckBoxBonanza(p, 0.05, self.on_checkbox_active)
            cbb.ids.checker.group = "check yo self before you wreck yo self"
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
            self.listener.bind_slave_to_presentation(self.presentation, self.selected_slave)
            self.button.text = self.button.text.split("\n")[0] + "\n" + self.selected_slave






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

class RemovePresentationsPopUp(Popup, EventDispatcher):
    """
    A kivy popup that allows the user to remove made presentations in master mode
    """

    def __init__(self, presentations, listener):

        super(RemovePresentationsPopUp,self).__init__()
        self.populate_presentation_list(presentations)
        self.selected_presentations=[]
        self.listener=listener

    def populate_presentation_list(self, presentations):
        """
        adds the checkboslist and corresponding presentation list to RemovePresentationPopUp
        :param presentations:
        :return:
        """
        presentation_list = self.ids.presentation_list
        for p in presentations:
            presentation_list.add_widget(CheckBoxBonanza(p, 0.05, self.on_checkbox_active))

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


class FileSavingDialogPopUp(Popup):
    """
    A popup functionality to confirm actions
    when copying a file that already exists.
    """
    COPY_EXTENSION = "_copy"    # the string to use when prefilling
                                # the name for copied file
    destination = StringProperty('')
    new_filename = StringProperty('')
    original_destination_filename_only = StringProperty('')

    """
    This list contains all characters that are reserved when naming a file
    either in Unix or Windows
    """
    RESERVED_FILENAME_CHARS = ["/", "\\", "?", "%", "*", ":", "|", '"', "<", ">"]

    def __init__(self, source, destination, filename_list, listener, media_path):
        """
        The source and destination files are passed as arguments
        :param source: a string, the source file with path
        :param destination: a string, the destination file with path
        :param filename_list: the list to append the created filename
        """
        super(FileSavingDialogPopUp, self).__init__()
        self.source = source
        self.destination_name = destination
        self.destination = destination
        self.media_path = media_path
        self.media_files = [file for file in os.listdir(self.media_path) if
                            os.path.isfile(os.path.join(self.media_path, file))]
        self.new_filename = self.__prefilled_new_file_name(destination)
        self.original_destination_filename_only = self.__parse_filename_only(destination)
        self.ids.save_as.bind(text=self.on_text)
        self.filename_list = filename_list
        self.listener = listener

    def __parse_filename_only(self, filepath):
        """
        A private helper method to return the file name from a
        "path1/path2/path3/filename.ext" string.
        :param filepath: a string, the pathpathpathfile-thingy
        :return: a string the file name only
        """
        paths_and_file_list = filepath.split(os.sep)
        return paths_and_file_list[len(paths_and_file_list) - 1]

    def on_text(self, instance, filename):
        """
        This function is called every time the bound widget's text-property changes
        :param instance: the instance of the Widget
        :param filename: the value in the text property
        :return:
        """
        copy_file_btn = self.ids.copy_file_button
        if not filename or filename in self.media_files \
                or self.__contains_reserved_chars(filename):
            copy_file_btn.disabled = not False
        else:
            copy_file_btn.disabled = not True

    def __contains_reserved_chars(self, filename):
        """
        Checks if the given filename contains any reserved characters
        :param filename: a string, the file's name
        :return: a boolean, True if reserved characters were encountered, False otherwise
        """
        for reserved_char in self.RESERVED_FILENAME_CHARS:
            if reserved_char in filename:
                return True

        return False

    def __prefilled_new_file_name(self, destination):
        """
        A private method to create a prefilled filename based on
        the original destination filename. The filename will differ
        from all the file names currently in the app's media folder
        :param destination: a string, the destination as "path1/path2/filename.ext"
        :return: a string, prefilled filename
        """
        separated_path_list = destination.split(os.sep)
        filename_and_extension = separated_path_list[len(separated_path_list) - 1].split('.')
        filename_copy = ''
        if len(filename_and_extension) > 1:
            filename_copy = self.__create_filename_with_extensions(filename_and_extension)
        else:
            filename_copy += filename_and_extension[0] + self.COPY_EXTENSION
        return filename_copy

    def __create_filename_with_extensions(self, filename_and_extensions):
        """
        A private helper methos. Creates a file name based on the filename
        and its extensions
        :param filename_and_extensions: a list, first element is the filename, the rest are its extensions
        :return: a string, a filename with extensions
        """
        extensions = filename_and_extensions[1:len(filename_and_extensions)]
        filename_with_extensions = filename_and_extensions[0]
        while self.__current_filename_with_extensions(filename_with_extensions, extensions) in self.media_files:
            filename_with_extensions += self.COPY_EXTENSION
        for i in range(0, len(extensions)):
            filename_with_extensions += '.' + extensions[i]
        return filename_with_extensions

    def __current_filename_with_extensions(self, filename, extensions):
        """
        A private helper method. Returns the filename and its extensions.
        :param filename: a string, the file's name
        :param extensions: a list, the extensions
        :return: a string, a filename with extensions
        """
        filename_with_extensions = filename
        for i in range(0, len(extensions)):
            filename_with_extensions += '.' + extensions[i]
        return filename_with_extensions

    def replace_file(self):
        """
        Replaces the original destination file.
        :return: None
        """
        self.copy_file_as(self.destination_name)

    def create_new_file(self):
        """
        Creates a new file.
        :return: None
        """
        separated_path_list = self.destination_name.split(os.sep)
        separated_path_list[len(separated_path_list) - 1] = self.ids.save_as.text
        file_to_save = separated_path_list[0]
        for i in range(1, len(separated_path_list)):
            file_to_save += os.sep + separated_path_list[i]
        self.copy_file_as(file_to_save)

    def copy_file_as(self, filename):
        """
        Copies the source file to to another location.
        :param filename: the file to write
        :return: None
        """
        try:
            copy(self.source, filename)
            self.filename_list.append(filename)
            self.listener.notify_file_import()
        except Exception as ex:
            ExceptionAlertPopUp("Error writing file", ex).open()


class ExceptionAlertPopUp(Popup):
    error_msg = StringProperty('')
    error_title = StringProperty('')

    def __init__(self, title, exception):
        super(ExceptionAlertPopUp, self).__init__()
        self.error_title = title
        self.error_msg = exception.__class__.__name__ + ": " + str(exception)