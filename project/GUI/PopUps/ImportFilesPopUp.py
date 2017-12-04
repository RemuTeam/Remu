import os
from shutil import copyfile

from Constants.TestReturnValue import *
from kivy.event import EventDispatcher

from Constants.SupportedFileTypes import AllSupportedFormats
from Constants.FileHandlingMode import ImportMultipleFiles
from GUI.PopUps.FileSavingDialogPopUp import FileSavingDialogPopUp
from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp


class ImportFilesPopUp(FileHandlerPopUp, EventDispatcher):
    """
    A file selection and opening popup
    """

    def __init__(self, listener, imported_files, presentations,
                 selected_presentations, media_path, test_mode=False):
        """
        Constructor

        :param listener: the component to inform about file imports
        :param imported_files: a kivy ListProperty to store files that are imported
        :param presentations: a list of Presentation names
        :param
        """
        super(ImportFilesPopUp, self).__init__(title="Import files",
                                               imported_files=imported_files,
                                               default_path=media_path,
                                               callback=self.import_files_for_presentation,
                                               file_handling_mode=ImportMultipleFiles,
                                               callback_button_text="Import",
                                               filters=AllSupportedFormats,
                                               selected_presentations=selected_presentations,
                                               presentation_names=presentations)
        self.media_path = media_path
        self.listener = listener
        self.test_mode = test_mode

    def import_files_for_presentation(self, path, selection, savefilename):
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