from kivy.event import EventDispatcher

from GUI.PopUps.FileHandlerPopUp import FileHandlerPopUp


class ProjectSavePopUp(FileHandlerPopUp, EventDispatcher):
    """
    A file selection and opening popup
    """

    def __init__(self, listener, project_path, test_mode=False):
        """
        Constructor

        :param listener: the component to inform about file imports
        :param imported_files: a kivy ListProperty to store files that are imported
        :param presentations: a list of Presentation names
        :param
        """
        super(ProjectSavePopUp, self).__init__(title="Save project",
                                               default_path=project_path,
                                               callback=self.save_project,
                                               callback_button_text="Save",
                                               multiselect=False)
        self.project_path = project_path
        self.listener = listener
        self.test_mode = test_mode

    def save_project(self, path, filename):
        """
        PLEASE IMPLEMENT ASAP!
        :param path:
        :param filename:
        :return:
        """
        pass
