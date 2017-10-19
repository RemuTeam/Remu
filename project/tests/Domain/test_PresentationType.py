import unittest
from Domain.PresentationType import PresentationType

class TestPresentationType(unittest.TestCase):
    def test_image_value_is_zero(self):
        self.assertEqual(PresentationType.Image.value, 0)

    def test_text_value_is_zero(self):
        self.assertEqual(PresentationType.Text.value, 1)
