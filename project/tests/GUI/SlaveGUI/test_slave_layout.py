
import unittest
from GUI.SlaveGUI.SlaveGUILayout import SlaveGUILayout


class SlaveLayoutTest(unittest.TestCase):
    def setUp(self):
        self.slave_layout = SlaveGUILayout()
        self.new_info_text = "mukamakajugajaga"

    def test_set_info_text(self):
        self.assertNotEqual(self.slave_layout.info_text, self.new_info_text)
        self.slave_layout.set_info_text(self.new_info_text)
        self.assertEqual(self.slave_layout.info_text, self.new_info_text)
