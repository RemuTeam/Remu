"""
import unittest
from GUI.GUIFactory import SlaveGUILayout


class SlaveLayoutTest(unittest.TestCase):
    def setUp(self):
        self.slave_layout = SlaveGUILayout()

    def test_is_not_shown_at_first(self):
        self.assertFalse(self.slave_layout.showpic)
        self.assertEqual(self.slave_layout.ids.picture.source, None)

    def test_show_pic_is_true_after_button_pressed(self):
        self.slave_layout.button_pressed()
        self.assertTrue(self.slave_layout.showpic)
        self.assertEqual(self.slave_layout.ids.picture.source, 'a.jpg')

    def test_show_pic_is_false_again_after_button_pressed_two_times(self):
        self.slave_layout.button_pressed()
        self.slave_layout.button_pressed()
        self.assertFalse(self.slave_layout.showpic)
        self.assertEqual(self.slave_layout.ids.picture.source, '')


if __name__ == '__main__':
    unittest.main()
"""