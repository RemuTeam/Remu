import os
import unittest

from Constants.PathConstants import PathConstants

from Constants.MessageKeys import MessageKeys
from Domain.Presentation import Presentation


class PresentationTest(unittest.TestCase):
    def setUp(self):
        self.presentation = Presentation()
        self.presentation_filenames = ["a.jpg", "g.mp4", "test_text.txt"]

    def set_presentation_elements(self, presentation_filenames):
        self.presentation.set_source_folder(PathConstants.TEST_MEDIA_FOLDER)
        self.presentation.set_files(presentation_filenames)
        self.presentation.get_presentation_elements_from_path()

    def test_init_works_as_inteded(self):
        self.assertEqual(self.presentation.get_presentation_content(), [])
        self.assertEqual(self.presentation.presentation_elements, [])
        self.assertEqual(-1, self.presentation.index)
        self.assertEqual(self.presentation.media_path, PathConstants.MEDIA_FOLDER)

    def test_get_presentation_elements_from_path(self):
        self.set_presentation_elements(self.presentation_filenames)
        self.assertEqual(self.presentation_filenames, self.presentation.get_presentation_content())
        self.presentation.get_presentation_elements_from_path()
        self.assertEqual(len(self.presentation.presentation_elements), 3)
        for i in range(0, len(self.presentation.presentation_elements)):
            self.assertEqual(self.presentation.presentation_elements[i].source_file,
                             os.path.join(PathConstants.TEST_MEDIA_FOLDER, self.presentation_filenames[i]))

    def test_pic_file_is_supported(self):
        pic_file = os.path.join(PathConstants.TEST_MEDIA_FOLDER, "a.jpg")
        self.assertTrue(Presentation.filetype_is_supported(pic_file))

    def test_not_pic_file_is_not_supported(self):
        not_pic_file = os.path.join(PathConstants.TEST_MEDIA_FOLDER, "test_text.txt")
        self.assertFalse(Presentation.filetype_is_supported(not_pic_file))

    def test_get_function_when_presentation_elements_is_none(self):
        self.assertIsNone(self.presentation.get(0))

    def test_get_function_lower_boundary(self):
        self.set_presentation_elements(self.presentation_filenames)
        self.assertIsNone(self.presentation.get(-1))

    def test_get_function_upper_boundary(self):
        self.set_presentation_elements(self.presentation_filenames)
        self.assertIsNone(self.presentation.get(len(self.presentation_filenames)))

    def test_get_first_element(self):
        self.set_presentation_elements(self.presentation_filenames)
        self.assertEqual(self.presentation.get(0).source_file,
                         os.path.join(PathConstants.TEST_MEDIA_FOLDER, self.presentation_filenames[0]))

    def test_get_last_element(self):
        self.set_presentation_elements(self.presentation_filenames)
        self.assertEqual(self.presentation.get(len(self.presentation.presentation_elements) - 1).source_file,
                         os.path.join(PathConstants.TEST_MEDIA_FOLDER, self.presentation_filenames[len(self.presentation_filenames) - 1]))

    def test_get_message_dictionary(self):
        self.set_presentation_elements(self.presentation_filenames)
        dickie = self.presentation.get_message_dictionary()
        self.assertEqual(dickie[MessageKeys.index_key], -1)
        self.assertEqual(dickie[MessageKeys.presentation_content_key], self.presentation_filenames)
        self.presentation.get_next()
        dickie = self.presentation.get_message_dictionary()
        self.assertEqual(dickie[MessageKeys.index_key], 0)
        self.assertEqual(dickie[MessageKeys.presentation_content_key], self.presentation_filenames)
