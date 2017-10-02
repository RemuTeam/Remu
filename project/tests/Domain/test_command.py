import unittest
from Domain.Command import Command

class CommandTest(unittest.TestCase):
    def test_REQUEST_PRESENTATION_is_zero(self):
        self.assertEqual(Command.REQUEST_PRESENTATION.value, 0)

    def test_SHOW_NEXT_is_one(self):
        self.assertEqual(Command.SHOW_NEXT.value, 1)

