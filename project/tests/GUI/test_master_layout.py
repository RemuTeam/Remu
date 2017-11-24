import unittest
from GUI.GUIFactory import MasterGUILayout


class MasterLayoutTests(unittest.TestCase):
    def setUp(self):
        self.presentations = ["a", "b", "c"]
        self.import_to_presentations = ["a", "b"]
        self.import_files = ["c.jpg", "d.txt"]
        self.gui = MasterGUILayout()
        self.slave_overview = self.gui.ids.slave_overview
        self.slave_presentations = self.slave_overview.ids.slave_presentations
        for pres in self.presentations:
            self.slave_overview.new_presentation_to_overview(pres)
        self.gui.import_to_presentations = self.import_to_presentations
        self.gui.import_list = self.import_files

    def assertImportCounterValue(self, value):
        self.assertEqual(self.gui.import_counter, value)

    def assertCounterReset(self):
        self.assertImportCounterValue(-1)

    def test_file_import_counter_is_resetted_in_init(self):
        self.assertCounterReset()

    def test_file_import_counter_updates_correctly(self):
        self.gui.import_started(len(self.gui.import_list))
        self.assertImportCounterValue(len(self.gui.import_list))
        self.gui.notify_file_import()
        self.assertImportCounterValue(len(self.gui.import_list) - 1)
        self.gui.notify_file_import()
        self.assertCounterReset()
        self.assertEqual(len(self.slave_presentations.children[0].visuals), 0)
        self.assertEqual(len(self.slave_presentations.children[1].visuals), 2)
        self.assertEqual(len(self.slave_presentations.children[2].visuals), 2)
