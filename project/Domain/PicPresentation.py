import os
from PIL import Image
from Domain.Presentation import Presentation

"""
This class contains the data and functionality 
of a picture presentation
"""


class PicPresentation(Presentation):
    IMAGE_PATH = "images"

    """
    Construct the presentation
    """
    def __init__(self):
        self.pic_files = []
        self.pic_index = 0

    """
    Loads the pictures to the presentation
    The directory to load the files from is "images"
    """
    def __get_filenames(self):
        if len(self.pic_files) == 0:
            path = os.path.join(os.getcwd(), self.IMAGE_PATH)
            self.get_pics_from_path(path)

    """
    Gets supported files' names from the path given
    as parameter
    """
    def get_pics_from_path(self, path):
        for filename in os.listdir(path):
            relative_filename = self.IMAGE_PATH + "/" + filename
            if self.filetype_is_supported(relative_filename):
                self.pic_files.append(relative_filename)

        self.pic_files.sort()

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
        return self.get(self.pic_index)

    """
    Returns the image file of the index
    Returns None if the list has no such index
    
    index:  an integer, the index of the image file
    """
    def get(self, index):
        if -1 < index < len(self.pic_files):
            next_file = self.pic_files[index]
            self.pic_index = index + 1
            return next_file
        else:
            return None

    """
    Resets the picture presentation to start from the beginning
    """
    def reset(self):
        self.pic_index = 0

    """
    Loads the presentation's elements and resets the presentation
    """
    def load(self):
        self.__get_filenames()
        self.reset()

    """
    Empties the list of image files and reloads them again
    without resetting the presentation
    """
    def reload(self):
        del self.pic_files[:]
        self.__get_filenames()