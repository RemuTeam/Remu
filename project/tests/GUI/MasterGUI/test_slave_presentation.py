import unittest
from GUI.MasterGUI.SlavePresentation import SlavePresentation
from GUI.MasterGUI.SlavePresentation import SlaveVisualProperty
from Domain.Presentation import Presentation

class TestSlavePresentation(unittest.TestCase):
    def setUp(self):
        self.filepath1 = "fruitful/workflow/is/nice.jpg"
        self.filename1 = "nice.jpg"
        self.filename2 = self.a_hundred_chars_long_string()
        self.filename3 = "somethingmorepleasantthanscreaming.mp4"
        self.pres = Presentation()
        self.layout = SlavePresentation(self.pres)
        self.draggable_element = SlaveVisualProperty("nice.jpg")

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

    def test_getting_presentation_from_widgets(self):
        self.layout.update_presentation_content([self.filepath1, self.filename3])
        pres = self.layout.get_presentation_from_widgets()
        self.assertListEqual(self.pres.presentation_filenames, pres.presentation_filenames)

    def test_sorting(self):
        self.layout.update_presentation_content([self.filepath1, self.filename3])
        self.layout.visuals[0].x = 5000
        self.layout.sort()
        self.assertListEqual(self.pres.presentation_filenames, [self.filename3, self.filepath1.split("/")[-1]])

    def test_on_x(self):
        self.draggable_element.parent = self.layout
        self.draggable_element.x = 5000
        self.draggable_element.width = 30
        self.draggable_element.being_moved = True
        self.draggable_element.on_x()
        self.assertEqual(self.draggable_element.x, 5000)

    def test_requiring_update(self):
        self.draggable_element.parent = self.layout
        self.draggable_element.x = 5000
        self.draggable_element.width = 30
        self.draggable_element.old_x = 4964
        self.assertTrue(self.draggable_element.is_update_required())
        self.draggable_element.old_x = 5036
        self.draggable_element.going_forward = False
        self.assertTrue(self.draggable_element.is_update_required())