import unittest
from GUI.GUIFactory import ImportFilesPopUp

class TestImportFilesPopup(unittest.TestCase):
    def setUp(self):
        self.popup = ImportFilesPopUp(None, None, ["apa", "paa"], None)

    def test_sumthin(self):
        self.assertTrue(True)