from enum import IntEnum

"""
An enum to specify the type of a Presentation
"""
class PresentationType(IntEnum):
    Image = 0   # for PicPresentations
    Text = 1    # for TextPresentations