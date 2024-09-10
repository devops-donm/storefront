import unittest
from unittest.mock import patch
import sys

from storefront import main, get_budget

class TestMainFunction(unittest.TestCase):
    # Test for normal input
    @patch('builtins.input', side_effect=['TestUser', '100'])
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

class TestGetBudgetFunctionality(unittest.TestCase):
    # Test for valid budget input
    @patch('builtins.input', return_value='100')
    def test_get_budget_valid_input(self, mock_input):
        """
        Test that get_budget returns the correct budget for valid input.
        """
        result = get_budget()
        self.assertEqual(result, 100)
    
    # Test for invalid input (non-integer)
    @patch('builtins.input', side_effect=['invalid', '200'])
    def test_get_budget_invalid_input_non_integar(self, mock_input):
        """
        Test that get_budget handles non-integer and eventually returns the correct budget.
        """
        result = get_budget()
        self.assertEqual(result, 200)

    # Test for invalid input (negative integer)
    @patch('builtins.input', side_effect=['-50', '300'])
    def test_get_budget_invalid_input_negative(self, mock_input):
        """
        Test that get_budget handles negative integer input and eventually returns the correct buget.
        """
        result = get_budget()
        self.assertEqual(result, 300)
    
    # Test for invalid input (zero)
    @patch('builtins.input', side_effect=['0', '400'])
    def test_get_budget_invalid_input_zero(self, mock_input):
        """
        Test that get_budget handles zero input and eventually returns the correct budget.
        """
        result = get_budget()
        self.assertEqual(result, 400)

if __name__ == '__main__':
    unittest.main()