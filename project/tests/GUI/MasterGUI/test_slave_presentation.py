import unittest
from GUI.MasterGUI.SlavePresentation import SlavePresentation
from Domain.Presentation import Presentation

class TestSlavePresentation(unittest.TestCase):
    def setUp(self):
        self.filepath1 = "fruitful/workflow/is/nice.jpg"
        self.filename1 = "nice.jpg"
        self.filename2 = self.a_hundred_chars_long_string()
        self.pres = Presentation()
        self.layout = SlavePresentation(self.pres)

    def a_hundred_chars_long_string(self):
        string = ""
        for i in range(100):
            string += "A"
        return string

    def test_filename1(self):
        visual_count = len(self.layout.visuals)
        self.layout.create_visual_widgets([self.filepath1])
        self.assertEqual(self.layout.visuals[visual_count].visual_name, self.filename1)

    def test_filename2(self):
        visual_count = len(self.layout.visuals)
        self.layout.create_visual_widgets([self.filename2])
        self.assertTrue(self.layout.visuals[visual_count].visual_name.endswith("..."))