"""
Contains the info of a picture presentation
"""


class PicPresentation:
    pic_files = []
    pic_index = 0

    """
    Construct the presentation
    """
    def __init__(self):
        self.load_pics()

    """
    Loads the pictures to the presentation
    """
    def load_pics(self):
        if len(self.pic_files) == 0:
            self.pic_files.append('a.jpg')
            self.pic_files.append('b.png')

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
