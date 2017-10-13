import unittest
from Domain.PicPresentation import PicPresentation

class PicPresentationTest(unittest.TestCase):
    pic_presentation = None

    def setUp(self):
        self.pic_presentation = PicPresentation()
        self.pic_presentation.get_filenames()

    def test_get_first_pic(self):
        self.assertCountEqual(self.pic_presentation.get_next(), 'images/a.jpg')

    def test_get_second_pic(self):
        self.pic_presentation.get_next()
        self.assertCountEqual(self.pic_presentation.get_next(), 'images/b.jpg')

    def test_no_pics(self):
        for i in range(0, len(self.pic_presentation.pic_files)):
            self.pic_presentation.get_next()
        self.assertIsNone(self.pic_presentation.get_next())

    def test_reset(self):
        self.pic_presentation.get_next()
        self.assertEqual(self.pic_presentation.pic_index, 1)
        self.pic_presentation.reset()
        self.assertEqual(self.pic_presentation.pic_index, 0)