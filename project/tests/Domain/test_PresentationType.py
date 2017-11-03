import unittest
from Domain.ContentType import ContentType

class TestPresentationType(unittest.TestCase):
    def test_image_value_is_zero(self):
        self.assertEqual(ContentType.Image.value, 0)

    def test_text_value_is_zero(self):
        self.assertEqual(ContentType.Text.value, 1)
