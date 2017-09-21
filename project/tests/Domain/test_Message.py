import unittest

from Domain.Message import Message


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
        self.assertEqual(msg.get_field("Test"), "Kappa")


if __name__ == '__main__':
    unittest.main()