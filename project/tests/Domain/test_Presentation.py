import unittest
from Domain.Presentation import Presentation

class TestPresentation(unittest.TestCase):
    def setUp(self):
        self.presentation = PresentationImpl()

    def test_get_presentation_type(self):
        self.assertIsNone(self.presentation.get_presentation_type())

class PresentationImpl(Presentation):
    pass