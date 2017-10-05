from Domain.Slave import Slave
from Domain.Message import Message
from Domain.Command import Command
from RemuTCP.RemuTCP import RemuTCP
import unittest
from unittest.mock import Mock

class SlaveTest(unittest.TestCase):
    def test_init_with_no_connection(self):
        slave = Slave()
        self.assertIsNone(slave.master_connection)
        self.assertIsNotNone(slave.presentation)

    def test_init_with_connection(self):
        mock = Mock(RemuTCP)
        slave = Slave(mock)
        self.assertEqual(slave.master_connection, mock)

    def test_handling_picpresentation_request(self):
        slave = Slave()
        msg = Message()
        msg.set_field("type", "command")
        msg.set_field("command", Command.REQUEST_PRESENTATION.value)
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field("data")["pic_index"], 0)
        self.assertCountEqual(response.get_field("data")["pic_files"], ["images/a.jpg", "images/b.jpg"])

    def test_handling_show_next(self):
        slave = Slave()
        msg = Message()
        msg.set_field("type", "command")
        msg.set_field("command", Command.SHOW_NEXT.value)
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field("responseTo"), Command.SHOW_NEXT.value)
        self.assertEqual(slave.presentation.pic_index, 1)

    def test_handling_invalid_commands(self):
        slave = Slave()
        msg = Message()
        msg.set_field("command", "SHOWUSWHATYOU'VEGOT")
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field("responseTo"), Command.INVALID_COMMAND.value)