import unittest
import os


class MainTest(unittest.TestCase):
    timeout_in_seconds = 2
    main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_file = "Main.py"

    def get_command_with_arguments(self, argv):
        command = "timeout --preserve-status -sSIGTERM "
        command += str(self.timeout_in_seconds) + "s python3 "
        command += os.path.join(self.main_path, self.main_file)

        for arg in argv:
            command += " " + str(arg)

        return command

    def test_without_parameters(self):
        return_value = os.system(self.get_command_with_arguments([]))
        self.assertEqual(0, return_value)

    def test_with_one_parameter(self):
        return_value = os.system(self.get_command_with_arguments(["master"]))
        self.assertEqual(0, return_value)

    def test_with_two_parameters(self):
        return_value = os.system(self.get_command_with_arguments(["master" "0.0.0.0"]))
        self.assertEqual(0, return_value)

    def test_with_three_parameters(self):
        return_value = os.system(self.get_command_with_arguments(["master" "0.0.0.0", "too_many_args"]))
        self.assertEqual(0, return_value)
