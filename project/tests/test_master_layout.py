import unittest
from GUI.GUIFactory import MasterGUILayout

class MasterLayoutTests(unittest.TestCase):

    def test_messages_sent_is_zero_at_start(self):
        layout = MasterGUILayout()
        self.assertEquals(0, layout.msg_sent)


    def test_messages_sent_is_incremented_properly(self):
        layout = MasterGUILayout()
        layout.increment()
        self.assertEquals(1, layout.msg_sent)


if __name__ == '__main__':
    unittest.main()