import os
import unittest
from Domain.TextPresentation import TextPresentation
from Domain.ContentType import ContentType
from Domain.WorkingDirectories import WorkingDirectories

class TextPresentationTest(unittest.TestCase):

    def setUp(self):
        filename = "test_text.txt"
        filename2 = "test_text2.txt"
        pathname = WorkingDirectories.TEST_MEDIA_FOLDER
        self.tp = TextPresentation()
        self.tp.set_source_folder(WorkingDirectories.TEST_MEDIA_FOLDER)
        self.textfile = os.path.join(os.getcwd(), pathname, filename)
        self.textfile2 = os.path.join(os.getcwd(), pathname, filename2)

    def set_filename(self, filename):
        self.tp.set_text_file_path_and_name(filename)

    def load(self):
        self.set_filename(self.textfile)
        self.tp.load()

    def test_init(self):
        self.assertEqual(len(self.tp.presentation_content), 0)
        self.assertEqual(self.tp.index, 0)

    def test_set_text_file_path_and_name(self):
        self.set_filename(self.textfile)
        self.assertEqual(self.tp.textfile, self.textfile)

    def test_load(self):
        self.load()
        self.assertEqual(len(self.tp.presentation_content), 2)

    def test_get_next(self):
        self.load()
        ok = self.tp.get_next().startswith("Well, the way they make shows is")
        self.assertTrue(ok)
        self.assertEqual(self.tp.index, 1)
        ok = self.tp.get_next().startswith("akak")
        self.assertTrue(ok)
        self.assertEqual(self.tp.index, 2)

    def test_get_out_of_boundaries_1(self):
        self.load()
        self.assertEqual(self.tp.get(-1), "")
        self.assertEqual(self.tp.index, 0)

    def test_get_out_of_boundaries_2(self):
        self.load()
        self.assertEqual(self.tp.get(4), "")
        self.assertEqual(self.tp.index, 0)

    def test_get_inside_boundaries_1(self):
        self.load()
        ok = self.tp.get(0).startswith("Well, the way they make shows is")
        self.assertTrue(ok)
        self.assertEqual(self.tp.index, 1)

    def test_get_inside_boundaries_2(self):
        self.load()
        ok = self.tp.get(1).startswith("akak")
        self.assertTrue(ok)
        self.assertEqual(self.tp.index, 2)

    def test_reset(self):
        self.load()
        self.tp.get_next()
        self.assertEqual(self.tp.index, 1)
        self.tp.reset()
        self.assertEqual(self.tp.index, 0)

    def test_reload(self):
        self.load()
        ok = self.tp.get_next().startswith("Well, the way they make shows is")
        self.assertTrue(ok)
        self.set_filename(self.textfile2)
        self.tp.reload()
        next_text = self.tp.get_next()
        print(next_text)
        ok = next_text.startswith("akak")
        self.assertTrue(ok)

    def test_load_again(self):
        self.load()
        ok = self.tp.get_next().startswith("Well, the way they make shows is")
        self.assertTrue(ok)
        self.assertEqual(self.tp.index, 1)
        self.tp.load()
        self.assertEqual(self.tp.index, 0)
        ok = self.tp.get_next().startswith("Well, the way they make shows is")
        self.assertTrue(ok)
        self.assertEqual(self.tp.index, 1)

    def test_get_presentation_type(self):
        self.assertEqual(self.tp.get_presentation_type(), ContentType.Text)

    def test_get_presentation_content(self):
        self.assertEqual(self.tp.get_presentation_content(), self.tp.presentation_content)
