import unittest
from GUI.MasterGUI.MasterGUILayout import MasterGUILayout

class MockClass:

    def send_presentations_to_slaves(self):
        pass

    def end_presentation(self):
        pass


class MasterLayoutTests(unittest.TestCase):
    def setUp(self):
        self.presentations = ["a", "b", "c"]
        self.import_to_presentations = ["a", "b"]
        self.import_files = ["c.jpg", "d.txt"]
        self.gui = MasterGUILayout()
        self.project_overview = self.gui.ids.project_overview
        self.slave_presentations = self.project_overview.ids.slave_presentations
        for pres in self.presentations:
            self.project_overview.new_presentation_to_overview(pres)
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

    def test_create_new_presentation(self):
        presentation_name = "macaroon"
        self.gui.ids.txt_input.text = presentation_name
        self.assertEqual(self.gui.ids.txt_input.text, presentation_name)
        slave_btns_count = len(self.gui.project_overview.slave_buttons)
        self.gui.create_new_presentation(presentation_name)
        self.assertEqual(self.gui.ids.txt_input.text, "")
        self.assertEqual(len(self.gui.project_overview.slave_buttons), slave_btns_count + 1)

    def test_showing_multiple_widgets(self):
        btns = [self.gui.stop_pres_btn, self.gui.show_next_btn]
        for btn in btns:
            self.assertEqual(btn.opacity, 0)
            self.assertEqual(btn.size_hint_y, 0)
            self.assertEqual(btn.size_hint_x, 0)
        self.gui.change_visibility_of_multiple_elements(btns, False)
        for btn in btns:
            self.assertEqual(btn.opacity, 1)
            self.assertEqual(btn.size_hint_y, 1)
            self.assertEqual(btn.size_hint_x, 1)

    def test_presentation_disabled(self):
        presentation_disabled_unchanged = self.gui.presenting_disabled
        self.gui.start_presentation_button_disabled(not presentation_disabled_unchanged)
        self.assertFalse(self.gui.presenting_disabled == presentation_disabled_unchanged)

    def test_starting_presentation(self):
        self.gui.master = MockClass()
        self.gui.start_presentation()
        self.assertEqual(self.gui.start_pres_btn.opacity, 0)

    def test_stop_presentation(self):
        self.gui.master = MockClass()
        self.gui.stop_presentation()
        self.assertEqual(self.gui.start_pres_btn.opacity, 1)

    def test_get_presentation_list(self):
        list = self.gui.get_presentation_list()
        for item in self.presentations:
            self.assertTrue(item in list)

