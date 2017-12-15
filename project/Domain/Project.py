import json
from Domain.Presentation import Presentation
from kivy.logger import Logger
import Utils.FileHandler as fh
from Constants.PathConstants import PathConstants


class Project:
    """
    A project is a collection of presentations that should be shown simultaneously.
    """

    def __init__(self):
        """
        Creates an empty project, and initializes an empty list for presentations. Presentations are stored as a list of
        tuples, the first part of tuple being name of the presentation and the second part being an instance of
        presentation class.
        """
        self.presentations = []

    def remove_from_presentations(self, name):
        """
        Removes a single presentation by name. Assumes that the presentations are named uniquely.
        :param name: The name of the presentation that is deleted
        :return: Nothing
        """
        for presentation in self.presentations:
            if presentation[0] == name:
                self.presentations.remove(presentation)

    def dump_json(self):
        """
        Returns a json-formatted string representing the project.
        Presentation status is lost, only the presentation name and file contents are saved.
        This is intended to be used for saving the project as a file.
        :return: A json representation of the project.
        """
        # A list with presentation-objects replaced with the list of files in that project
        list_presentations = []
        for tuple in self.presentations:
            filenames = []
            for path in tuple[1].presentation_filenames:
                filenames.append(fh.get_filename_only(path))
            list_presentations.append((tuple[0], filenames))

        return json.dumps(list_presentations)

    def load_json(self, json_str):
        """
        Load project from JSON.

        :param json_str: JSON-formatted string representing a project.
        :return: Nothing
        """

        # project_list elements are tuples containing presentation name and file contents
        # The format is ["presentationname", ["file1", "file2", ...]"]
        project_list = json.loads(json_str)

        # create the real presentations by replacing file list with Presentation objects
        presentation_list = []
        for presentation_tuple in project_list:
            name = presentation_tuple[0]
            files = presentation_tuple[1]
            paths = []
            for file in files:
                path = fh.absolute_path(PathConstants.ABSOLUTE_MEDIA_FOLDER, file)
                paths.append(path)
            pres = Presentation(name)
            pres.presentation_filenames = paths
            presentation_list.append((name, pres))

        self.presentations = presentation_list
