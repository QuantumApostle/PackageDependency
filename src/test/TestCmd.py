import unittest
from io import StringIO
from unittest.mock import patch

from src.PackageManager import PackageManager


class MyTestCase(unittest.TestCase):

    def test_depend(self):
        package_manager = PackageManager()
        with patch('sys.stdout', new=StringIO()) as actual_out:
            input_cmd = "DEPEND A B"
            expected_output = ''
            package_manager._process_input(input_cmd)
            self.assertEqual(actual_out.getvalue(), expected_output)

    def test_install(self):
        package_manager = PackageManager()
        with patch('sys.stdout', new=StringIO()) as actual_out:
            input_cmd = "INSTALL A"
            expected_output = 'Installing A\n'
            package_manager._process_input(input_cmd)
            self.assertEqual(actual_out.getvalue(), expected_output)

    def test_cycle(self):
        package_manager = PackageManager()
        with patch('sys.stdout', new=StringIO()) as actual_out:
            input_cmd = [
                "DEPEND A B",
                "DEPEND B A"
            ]
            expected_output = 'A depends on B, ignoring command\n'
            for cmd in input_cmd:
                package_manager._process_input(cmd)
            self.assertEqual(actual_out.getvalue(), expected_output)

    def test_invalid_remove(self):
        package_manager = PackageManager()
        with patch('sys.stdout', new=StringIO()) as actual_out:
            input_cmd = [
                "REMOVE C"
            ]
            expected_output = 'C is not installed\n'
            for cmd in input_cmd:
                package_manager._process_input(cmd)
            self.assertEqual(actual_out.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
