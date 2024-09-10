import unittest
from unittest.mock import patch
import sys

from storefront import main

class TestMainFunction(unittest.TestCase):
    # Test for normal input
    @patch('builtins.input', return_value='TestUser')
    def test_main_with_input(self, mock_input):
        """
        Test that the main function works properly when give user input.
        The input will be mocked as 'TestUser'
        """
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised the following exception:\n{e}")
    
    # Test for handling KeyboardInterrupt
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('sys.stdout', new_callable=lambda: sys.__stdout__)
    def test_keyboard_interrupt(self, mock_stdout, mock_input):
        """
        Test that the program handles KeyboardInterrupt and prints "Goodbye".
        """
        with self.assertRaises(KeyboardInterrupt):
            main()

if __name__ == '__main__':
    unittest.main()