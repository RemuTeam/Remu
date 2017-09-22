import unittest
import os


class MainTest(unittest.TestCase):
    timeout_in_seconds = 2

    def test_without_parameters(self):
        return_value = os.system("timeout --preserve-status -sSIGTERM " +
                                 str(self.timeout_in_seconds) +
                                 "s python3 ~/Remu/project/Main.py")
        self.assertEqual(0, return_value)

    def test_with_one_parameter(self):
        return_value = os.system("timeout --preserve-status -sSIGTERM " +
                                 str(self.timeout_in_seconds) +
                                 "s python3 ~/Remu/project/Main.py master")
        self.assertEqual(0, return_value)

    def test_with_two_parameters(self):
        return_value = os.system("timeout --preserve-status -sSIGTERM " +
                                 str(self.timeout_in_seconds) +
                                 "s python3 ~/Remu/project/Main.py master 0.0.0.0")
        self.assertEqual(0, return_value)

    def test_with_three_parameters(self):
        return_value = os.system("timeout --preserve-status -sSIGTERM " +
                                 str(self.timeout_in_seconds) +
                                 "s python3 ~/Remu/project/Main.py master 0.0.0.0 too_much_params")
        self.assertEqual(0, return_value)
