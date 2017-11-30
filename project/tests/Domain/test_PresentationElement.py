import os
import unittest

from Constants.PathConstants import PathConstants

from Constants.ContentType import ContentType
from Domain.PresentationElement import PresentationElement


class TestPresentationElement(unittest.TestCase):
    def setUp(self):
        self.test_media_folder = os.path.join(os.getcwd(), PathConstants.TEST_MEDIA_FOLDER)
        self.text_source_file = os.path.join(self.test_media_folder, "test_text.txt")
        self.pic_source_file = os.path.join(self.test_media_folder, "a.jpg")
        self.text_element = PresentationElement(ContentType.Text, self.text_source_file)
        self.pic_element = PresentationElement(ContentType.Image, self.pic_source_file)

    def test_type_source_and_content_match_for_text_element(self):
        self.assertEqual(self.text_element.element_type, ContentType.Text)
        self.assertEqual(self.text_element.source_file, self.text_source_file)
        with open(self.text_source_file) as file:
            self.assertEqual(self.text_element.get_content(), file.read())

    def test_type_source_and_content_match_for_image_element(self):
        self.assertEqual(self.pic_element.element_type, ContentType.Image)
        self.assertEqual(self.pic_element.source_file, self.pic_source_file)
        self.assertEqual(self.pic_element.get_content(), self.pic_element.source_file)

    def test_eq_returns_false_if_class_does_not_match(self):
        self.assertFalse(self.pic_element.__eq__("banana"))

    def test_eq_returns_false_if_type_does_not_match(self):
        self.assertFalse(self.pic_element.__eq__(self.text_element))

    def test_eq_returns_false_if_source_file_does_not_match(self):
        other_pic_element = PresentationElement(ContentType.Image, os.path.join(self.test_media_folder, "b.jpg"))
        self.assertFalse(self.pic_element.__eq__(other_pic_element))

    def test_eq_returns_true_if_source_file_matches(self):
        other_pic_element = PresentationElement(ContentType.Image, self.pic_source_file)
        self.assertTrue(self.pic_element.__eq__(other_pic_element))