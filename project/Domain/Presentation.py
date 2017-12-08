import os
from Constants.MessageKeys import MessageKeys
from Constants.PathConstants import PathConstants
from PIL import Image
from Constants.ContentType import ContentType
from Domain.PresentationElement import PresentationElement
from kivy.logger import Logger


class Presentation:
    """
    Presentation class contains the presentation elements and names of the files in separate lists. Presentation class
    is responsible for loading the content from the media folder, and acts as a mediator when the application asks for
    a presentation element to show in the GUI.
    """
    IMAGE_FORMATS = ["jpg", "png"]
    VIDEO_FORMATS = ["mp4"]
    TEXT_FORMATS = ["txt"]

    def __init__(self):
        """
        Construct the presentation
        """
        self.presentation_elements = []
        self.presentation_filenames = []
        self.index = -1
        self.media_path = PathConstants.MEDIA_FOLDER

    def __len__(self):
        """
        This function is called when len(presentation) is called.
        The length of a presentation is equal to the length of
        its presentation_filenames list.
        :return: a non-negative integer, the number of files
                 in the presentation
        """
        return len(self.presentation_filenames)

    def set_source_folder(self, path):
        """
        Primarily used for testing purposes, set_source_folder, changes media_path to the one given in the parameter.
        The presentation needs to be loaded again to work properly

        :param path: String, sets the path that contains files for the presentation
        :return: Nothing
        """
        self.media_path = path

    def __create_presentation(self):
        """
        Loads the pictures to the presentation
        The directory to load the files from is defined in PathConstants
        """
        Logger.info("Presentation: Creating presentation")
        if self.presentation_elements is None or len(self.presentation_elements) == 0:
            path = os.path.join(os.getcwd(), self.media_path)
            Logger.info("Media path: %s", path)
            self.get_presentation_elements_from_path()

    def get_presentation_elements_from_path(self):
        """
        Gets supported files' names from the path given
        as parameter
        """
        self.presentation_elements = []
        Logger.debug("Presentation: Creating the presentation elements from folder " + self.media_path)
        for filename in self.presentation_filenames:
            extension = filename.split(".")[-1]
            relative_filename = self.media_path + "/" + filename
            Logger.debug("Relative filename: %s", relative_filename)

            if extension in self.VIDEO_FORMATS:
                self.presentation_elements.append(PresentationElement(ContentType.Video, relative_filename))
            elif extension in self.IMAGE_FORMATS:
                self.presentation_elements.append(PresentationElement(ContentType.Image, relative_filename))
            elif extension in self.TEXT_FORMATS:
                self.presentation_elements.append(PresentationElement(ContentType.Text, relative_filename))
            else:
                Logger.error("Presentation: Unsupported filetype \"%s\" ", extension)

    @staticmethod
    def filetype_is_supported(filename):
        """
        Checks if the filename given as attribute is a pointer to
        a valid image file
        """
        try:
            with Image.open(filename) as test_image:
                pass
        except:
            return False
        return True

    def get_next(self):
        """
        Get the filename for the next picture
        Returns None if no more pictures are available
        """
        self.index += 1
        return self.get(self.index)

    def get(self, index):
        """
        Returns the image file of the index
        Returns None if the list has no such index

        index:  an integer, the index of the image file
        """
        if self.presentation_elements is not None:
            if -1 < index < len(self.presentation_elements):
                next_file = self.presentation_elements[index]
                return next_file
        return None

    def reset(self):
        """
        Resets the picture presentation to start from the beginning

        :return: Nothing
        """
        self.index = -1

    def load(self):
        """
        Loads the presentation's elements and resets the presentation
        """
        self.__create_presentation()
        self.reset()

    def reload(self):
        """
        Empties the list of image files and reloads them again
        without resetting the presentation
        """
        del self.presentation_elements[:]
        self.__create_presentation()

    def get_presentation_content(self):
        """
        Request the content of the presentation
        """
        return self.presentation_filenames

    def get_message_dictionary(self):
        """
        Returns the presentation's content in a dictionary form. Useful when serializing the content into JSON.
        :return: Dictionarydis
        """
        dict = {}
        dict[MessageKeys.index_key] = self.index
        dict[MessageKeys.presentation_content_key] = self.get_presentation_content()
        return dict

    def set_files(self, filenamelist):
        """
        Sets the names of the files from a ready made list.
        """
        self.presentation_filenames = filenamelist