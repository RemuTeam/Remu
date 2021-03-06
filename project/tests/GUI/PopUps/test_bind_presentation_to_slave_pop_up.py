import unittest
from GUI.PopUps.BindPresentationToSlavePopUp import BindPresentationToSlavePopUp
from Domain.Master import Master
from GUI.MasterGUI.MasterGUILayout import MasterGUILayout
from unittest.mock import Mock
from kivy.uix.button import Button


class TestBindPresentationToSlavePopup(unittest.TestCase):

    def setUp(self):
        self.slave_name = "Slave"
        self.master = Master(Mock(MasterGUILayout))
        self.button = Button()
        self.bind_popup = BindPresentationToSlavePopUp([self.slave_name], None, self.master, self.button)

    def test_init_setups_properly(self):
        self.assertIsNone(self.bind_popup.presentation)
        self.assertEquals(self.bind_popup.listener, self.master)
        self.assertEquals(self.bind_popup.button, self.button)

    def test_checkbox_wont_select_if_no_boolean(self):
        self.bind_popup.on_checkbox_active(self.bind_popup.checkboxes[0].ids.checker, None)
        self.assertIsNone(self.bind_popup.selected_slave)

    def test_checkbox_selects(self):
        self.bind_popup.on_checkbox_active(self.bind_popup.checkboxes[0].ids.checker, True)
        self.assertEquals(self.bind_popup.selected_slave, self.slave_name)

    def test_confirm(self):
        self.bind_popup.confirm()
        self.assertEquals(self.button.text, '')

    #def test_confirm_just_works(self):
        # self.bind_popup.on_checkbox_active(self.bind_popup.checkboxes[0].ids.checker, True)
        # self.bind_popup.confirm()
        # self.assertEquals(self.button.text, self.slave_name)