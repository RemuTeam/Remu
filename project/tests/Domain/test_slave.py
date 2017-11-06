from Domain.Slave import Slave
from Domain.Message import Message
from Domain.Command import Command
from Domain.PresentationFactory import PresentationFactory
from Networking.RemuTCP import RemuTCP
from GUI.GUIFactory import PresentationLayout
from Domain.TextPresentation import TextPresentation
import unittest
from unittest.mock import Mock
from Domain.MessageKeys import MessageKeys
from unittest.mock import patch
from Domain.ContentType import ContentType
from Domain.PathConstants import PathConstants

class SlaveTest(unittest.TestCase):

    def setUp(self):
        self.slave = Slave()
        self.slave.presentation.set_source_folder(PathConstants.TEST_MEDIA_FOLDER)

    def test_init_with_no_layout(self):
        self.assertIsNone(self.slave.layout)
        self.assertIsNotNone(self.slave.presentation)

    def test_set_presentation(self):
        slave = Slave()
        slave.set_presentation(TextPresentation())
        self.assertEqual(slave.presentation.__class__.__name__, "TextPresentation")

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
        data_key = MessageKeys.presentation_content_key
        index_key = MessageKeys.index_key
        presentation = PresentationFactory.PicPresentation()
        presentation.set_source_folder(PathConstants.TEST_MEDIA_FOLDER)
        presentation.load()
        self.slave.set_presentation(presentation)
        msg = Message()
        msg.set_field(MessageKeys.type_key, "command")
        msg.set_field(MessageKeys.command_key, Command.REQUEST_PRESENTATION.value)
        response = self.slave.handle_message(msg)
        self.assertEqual(response.get_field(data_key)[index_key], 0)
        self.assertCountEqual(response.get_field(data_key)[MessageKeys.presentation_content_key],
                              presentation.get_presentation_content())

    def test_handling_show_next(self):
        slave = Slave(Mock(PresentationLayout))
        msg = Message()
        msg.set_field(MessageKeys.type_key, "command")
        msg.set_field(MessageKeys.command_key, Command.SHOW_NEXT.value)
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field(MessageKeys.response_key), Command.SHOW_NEXT.value)
        #self.assertEqual(slave.presentation.pic_index, 1)

    def test_handling_invalid_commands(self):
        slave = Slave()
        msg = Message()
        msg.set_field(MessageKeys.command_key, "SHOWUSWHATYOU'VEGOT")
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field(MessageKeys.response_key), Command.INVALID_COMMAND.value)

    def test_handling_empty_messages(self):
        slave = Slave()
        msg = Message()
        response = slave.handle_message(msg)
        self.assertEqual(response.get_field(MessageKeys.response_key), Command.INVALID_COMMAND.value)

    def test_handling_ending_presentation(self):
        slave = Slave()
        msg = Message()
        slave.layout = Mock(PresentationLayout)
        with patch.object(slave.layout, "reset_presentation") as mock:
            msg.set_field("command", Command.END_PRESENTATION.value)
            response = slave.handle_message(msg)
            self.assertEqual(response.get_field("responseTo"), Command.END_PRESENTATION.value)
            mock.assert_called_with()

    def test_handling_closing_connection(self):
        slave = Slave()
        msg = Message()
        slave.layout = Mock(PresentationLayout)
        with patch.object(slave.layout, "reset_presentation") as mock:
            msg.set_field("command", Command.DROP_CONNECTION.value)
            slave.handle_message(msg)
            mock.assert_called_with()

    def test_handling_show_next_resetting_presentation(self):
        slave = Slave()
        slave.set_presentation(PresentationFactory.PicPresentation())
        slave.presentation.load()
        for i in range(0, len(slave.presentation.get_presentation_content())):
            slave.presentation.get_next()
        msg = Message()
        slave.layout = Mock(PresentationLayout)
        with patch.object(slave.layout, "reset_presentation") as mock:
            msg.set_field(MessageKeys.command_key, Command.SHOW_NEXT.value)
            response = slave.handle_message(msg)
            self.assertEqual(response.get_field(MessageKeys.response_key), Command.SHOW_NEXT.value)
            mock.assert_called_with()
