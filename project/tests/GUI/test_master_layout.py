import unittest
from GUI.GUIFactory import MasterGUILayout


class MasterLayoutTests(unittest.TestCase):
    def setUp(self):
        self.gui = MasterGUILayout()

    def test_file_import_counter(self):
        self.assertEqual(self.gui.import_counter, -1)
