import unittest
from Domain.PicPresentation import PicPresentation
from Domain.PresentationType import PresentationType

class PicPresentationTest(unittest.TestCase):
    pic_presentation = None

    def setUp(self):
        self.pic_presentation = PicPresentation()
        self.pic_presentation.load()

    def test_get_first_pic(self):
        self.assertCountEqual(self.pic_presentation.get_next(), 'images/a.jpg')

    def test_get_second_pic(self):
        self.pic_presentation.get_next()
        self.assertCountEqual(self.pic_presentation.get_next(), 'images/b.jpg')

    def test_no_pics(self):
        self.pic_presentation.get_next()
        self.pic_presentation.get_next()
        self.assertIsNone(self.pic_presentation.get_next())

    def test_reset(self):
        self.pic_presentation.get_next()
        self.assertEqual(self.pic_presentation.index, 1)
        self.pic_presentation.reset()
        self.assertEqual(self.pic_presentation.index, 0)

    def test_reload(self):
        original_filenames = self.pic_presentation.presentation_content.copy()
        alternative_filenames = ["1.jpg", "2.jpg"]
        self.pic_presentation.presentation_content = alternative_filenames
        self.assertEqual(alternative_filenames, self.pic_presentation.presentation_content)
        self.pic_presentation.reload()
        self.assertEqual(original_filenames, self.pic_presentation.presentation_content)

    def test_get_filenames(self):
        alternative_filenames = ["1.jpg", "2.jpg"]
        self.pic_presentation.presentation_content = alternative_filenames
        self.assertEqual(alternative_filenames, self.pic_presentation.presentation_content)
        self.pic_presentation.load()
        self.assertEqual(alternative_filenames, self.pic_presentation.presentation_content)

    def test_get_presentation_type(self):
        self.assertEqual(self.pic_presentation.get_presentation_type(), PresentationType.Image)

    def test_get_presentation_content(self):
        self.assertEqual(self.pic_presentation.get_presentation_content(), self.pic_presentation.presentation_content)