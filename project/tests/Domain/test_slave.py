from Domain.Slave import Slave
from Domain.Message import Message
from Domain.Command import Command
from Networking.RemuTCP import RemuTCP
from GUI.GUIFactory import PresentationLayout
import unittest
from unittest.mock import Mock

class SlaveTest(unittest.TestCase):
    def test_init_with_no_layout(self):
        slave = Slave()
        self.assertIsNone(slave.layout)
        self.assertIsNotNone(slave.presentation)

    """
    def test_init_with_no_connection(self):
        slave = Slave()
        self.assertIsNone(slave.master_connection)
        self.assertIsNotNone(slave.presentation)

    
    def test_init_with_connection(self):
        mock = Mock(RemuTCP)
        slave = Slave(mock)
        self.assertEqual(slave.master_connection, mock)
    """

    def test_init_with_layout(self):
        mock = Mock(PresentationLayout)
        slave = Slave(mock)
        self.assertEqual(slave.layout, mock)

    def test_handling_picpresentation_request(self):
        slave = Slave()
        msg = Message()
        msg.set_field("type", "command")
        msg.set_field("command", Command.REQUEST_PRESENTATION.value)
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field("data")["pic_index"], 0)
        self.assertEqual(len(response.get_field("data")["pic_files"]), 5)

    def test_handling_show_next(self):
        slave = Slave(Mock(PresentationLayout))
        msg = Message()
        msg.set_field("type", "command")
        msg.set_field("command", Command.SHOW_NEXT.value)
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field("responseTo"), Command.SHOW_NEXT.value)
        #self.assertEqual(slave.presentation.pic_index, 1)

    def test_handling_invalid_commands(self):
        slave = Slave()
        msg = Message()
        msg.set_field("command", "SHOWUSWHATYOU'VEGOT")
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field("responseTo"), Command.INVALID_COMMAND.value)

    def test_handling_empty_messages(self):
        slave = Slave()
        msg = Message()
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field("responseTo"), Command.INVALID_COMMAND.value)
