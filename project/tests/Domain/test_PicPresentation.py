import unittest
from Domain.PicPresentation import PicPresentation

class PicPresentationTest(unittest.TestCase):
    pic_presentation = None

    def setUp(self):
        self.pic_presentation = PicPresentation()

    def test_get_first_pic(self):
        self.assertCountEqual(self.pic_presentation.get_next(), 'a.jpg')

    def test_no_pics(self):
        self.pic_presentation.get_next()
        self.assertIsNone(self.pic_presentation.get_next())