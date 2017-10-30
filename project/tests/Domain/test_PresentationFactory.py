import unittest
from Domain.PresentationFactory import PresentationFactory

class TestPresentationFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PresentationFactory()

    def test_text_presentation(self):
        presentation = self.factory.TextPresentation()
        self.assertEqual(presentation.__class__.__name__, "TextPresentation")

    def test_pic_presentation(self):
        presentation = self.factory.PicPresentation()
        self.assertEqual(presentation.__class__.__name__, "PicPresentation")