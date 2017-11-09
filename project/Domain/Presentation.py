import os
from PIL import Image
from Domain.PresentationElement import PresentationElement
from Domain.ContentType import ContentType
from Domain.PathConstants import PathConstants

"""
DEFINES A UNIFIED INTERFACE
FOR ALL SPECIALIZED PRESENTATIONS
"""
class Presentation:
    IMAGE_FORMATS = ["jpg"]
    VIDEO_FORMATS = ["mp4"]
    TEXT_FORMATS = ["txt"]

    def __init__(self):
        """
        Construct the presentation
        """
        self.presentation_content = []
        self.index = 0
        self.media_path = PathConstants.MEDIA_FOLDER  # vaihda PathConstants -viittaukseen

    def set_source_folder(self, path):
        """
        Primarily used for testing purposes, set_source_folder, changes MEDIA_PATH to the one given in the parameter.
        The presentation needs to be loaded again to work properly

        :param path: String, sets the path that contains files for the presentation
        :return: Nothing
        """
        self.media_path = path

    """
    Loads the pictures to the presentation
    The directory to load the files from is "images"
    """

    def __create_presentation(self):
        if len(self.presentation_content) == 0:
            path = os.path.join(os.getcwd(), self.media_path)
            print(path)
            self.get_presentation_elements_from_path(path)

    """
    Gets supported files' names from the path given
    as parameter
    """

    def get_presentation_elements_from_path(self, path):
        for filename in sorted(os.listdir(path)):
            extension = filename.split(".")[-1]
            relative_filename = self.media_path + "/" + filename
            print(relative_filename)

            if extension in self.VIDEO_FORMATS:
                self.presentation_content.append(PresentationElement(ContentType.Video, relative_filename))
            elif extension in self.IMAGE_FORMATS:
                self.presentation_content.append(PresentationElement(ContentType.Image, relative_filename))
            elif extension in self.TEXT_FORMATS:
                self.presentation_content.append(PresentationElement(ContentType.Text, relative_filename))
            else:
                print("Unsupported filetype: " + extension)

    """
    Checks if the filename given as attribute is a pointer to
    a valid image file
    """

    @staticmethod
    def filetype_is_supported(filename):
        try:
            with Image.open(filename) as test_image:
                pass
        except:
            return False
        return True

    """
    Get the filename for the next picture
    Returns None if no more pictures are available
    """

    def get_next(self):
        return self.get(self.index)

    """
    Returns the image file of the index
    Returns None if the list has no such index

    index:  an integer, the index of the image file
    """

    def get(self, index):
        if -1 < index < len(self.presentation_content):
            next_file = self.presentation_content[index]
            self.index = index + 1
            return next_file
        else:
            return None

    def reset(self):
        """
        Resets the picture presentation to start from the beginning

        :return: Nothing
        """
        self.index = 0

    """
    Loads the presentation's elements and resets the presentation
    """

    def load(self):
        self.__create_presentation()
        self.reset()

    """
    Empties the list of image files and reloads them again
    without resetting the presentation
    """

    def reload(self):
        del self.presentation_content[:]
        self.__create_presentation()

    """
    Request the content of the presentation
    """

    def get_presentation_content(self):
        content = []
        for presentation_element in self.presentation_content:
            content.append([presentation_element.source_file, presentation_element.type])
        return content

    def get_message_dictionary(self):
        dict = {}
        dict["index"] = self.index
        dict["presentation_content"] = self.get_presentation_content()
        return dict

    def add_elements(self, element_dict):
        content = element_dict["presentation_content"]
        for element in content:
            self.presentation_content.append(PresentationElement(element[1], element[0]))

    @staticmethod
    def CreatePresentation(entries):
        """
                Creates a Presentation based on the PresentationType given.
                Uses the parameter entries to update the presentation contents.
        """
        presentation = Presentation()
        presentation.add_elements(entries)

        return presentation