import os
from PIL import Image

"""
This class contains the data and functionality 
of a picture presentation
"""


class PicPresentation:
    pic_files = []
    pic_index = 0
    IMAGE_PATH = "images"

    """
    Construct the presentation
    """
    def __init__(self):
        pass

    """
    Loads the pictures to the presentation
    The directory to load the files from is "images"
    """
    def get_filenames(self):
        if len(self.pic_files) == 0:
            path = os.path.join(os.getcwd(), self.IMAGE_PATH)
            print(str(path))
            self.get_pics_from_path(path)

    """
    Gets supported files' names from the path given
    as parameter
    """
    def get_pics_from_path(self, path):
        for filename in os.listdir(path):
            relative_filename = self.IMAGE_PATH + "/" + filename
            print(str(relative_filename))
            if self.filetype_is_supported(relative_filename):
                self.pic_files.append(relative_filename)

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
        if self.pic_index < len(self.pic_files):
            next_file = self.pic_files[self.pic_index]
            self.pic_index += 1
            return next_file
        else:
            return None

    """
    Resets the picture presentation to start from the beginning
    """
    def reset(self):
        self.pic_index = 0