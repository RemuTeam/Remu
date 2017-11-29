from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from GUI.PopUps.PopUps import ExceptionAlertPopUp

import os
from shutil import copy

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