from Domain.TextPresentation import TextPresentation
from Domain.PicPresentation import PicPresentation

"""
Creates predefined presentation objects that inherit
Presentation interface
"""
class PresentationFactory:
    """
    Creates a TextPresentation and returns it
    """
    @staticmethod
    def TextPresentation():
        presentation = TextPresentation("texts/test_text.txt")
        return presentation

    """
    Creates a PicPresentation and returns it
    """
    @staticmethod
    def PicPresentation():
        presentation = PicPresentation()
        return presentation