import unittest

from Domain.Message import Message
from Domain.Command import Command

class TestMessageMethods(unittest.TestCase):

    def test_init(self):
        json_data = r'{"name": "test", "last": "case"}'
        msg = Message(json_data)
        self.assertEqual(msg.fields['name'],'test')
        self.assertEqual(msg.fields['last'],'case')

    def test_to_json(self):
        json_data = r'{"name": "test", "last": "case"}'
        msg = Message(json_data)
        json_data2 = msg.to_json()
        self.assertEqual(sorted(json_data), sorted(json_data2))

    def test_set_and_get_field(self):
        msg = Message()
        msg.set_field("Test", "Kappa")
        self.assertEqual(msg.fields["Test"], "Kappa")

    def test_get_field(self):
        msg = Message()
        msg.fields["Test"] = "Kappa"
        self.assertEqual(msg.fields["Test"], msg.get_field("Test"))

    def test_invalid_key(self):
        msg = Message()
        self.assertIsNone(msg.get_field("test"))

    def test_invalid_command(self):
        msg = Message()
        msg.set_field("command", "9999")
        self.assertEqual(Command.INVALID_COMMAND, msg.get_command())

    def test_no_data(self):
        msg = Message()
        self.assertIsNone(msg.get_data())

    def test_data(self):
        msg = Message()
        msg.set_field("data", "test")
        self.assertEqual(msg.get_data(), "test")

    def test_invalid_response(self):
        msg = Message()
        msg.set_field("responseTo", "9999")
        self.assertEqual(Command.INVALID_COMMAND, msg.get_response())

    def test_valid_response(self):
        msg = Message()
        msg.set_field("responseTo", 0)
        self.assertEqual(0, msg.get_response())


if __name__ == '__main__':
    unittest.main()