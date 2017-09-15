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
        self.assertDictEqual(json_data, json_data2)


if __name__ == '__main__':
    unittest.main()