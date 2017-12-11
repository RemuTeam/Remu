import unittest
from GUI.PopUps.RemovePresentationsPopUp import RemovePresentationsPopUp


class TestBindPresentationToSlavePopup(unittest.TestCase):

    def setUp(self):
        self.presentations = ["Slave1", "Slave2"]
        self.remove_popup = RemovePresentationsPopUp(self.presentations, None)

    def test_init_setups_properly(self):
        self.assertEquals(len(self.remove_popup.selected_presentations), 0)
        self.assertIsNone(self.remove_popup.listener)

    def test_init_populates_presentation_list_properly(self):
        self.assertEqual(len(self.remove_popup.ids.presentation_list.children), 2)

    def test_selected_presentations_is_empty_at_first(self):
        self.assertEqual(len(self.remove_popup.selected_presentations), 0)

    #
    # def test_checkbox_selects(self):
    #     self.bind_popup.on_checkbox_active(self.bind_popup.checkboxes[0].ids.checker, True)
    #     self.assertEquals(self.bind_popup.selected_slave, self.slave_name)
    #
    # def test_confirm(self):
    #     self.bind_popup.confirm()
    #     self.assertEquals(self.button.text, '')