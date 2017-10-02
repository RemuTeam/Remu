import unittest
from Domain.Command import *

class CommandTest(unittest.TestCase):
    def test_REQUEST_PRESENTATION_is_zero(self):
        self.assertEqual(Command.REQUEST_PRESENTATION.value, 0)

    def test_SHOW_NEXT_is_one(self):
        self.assertEqual(Command.SHOW_NEXT.value, 1)

    def test_INVALID_COMMAND_is_is_minus_one(self):
        self.assertEqual(Command.INVALID_COMMAND.value, -1)

    def test_PRESENTATION_UPDATE_is_zero(self):
        self.assertEqual(Notification.PRESENTATION_UPDATE.value, 0)

    def test_PRESENTATION_STATUS_CHANGE_is_one(self):
        self.assertEqual(Notification.PRESENTATION_STATUS_CHANGE.value, 1)

    def test_CONNECTION_FAILED_is_is_minus_one(self):
        self.assertEqual(Notification.CONNECTION_FAILED.value, -1)