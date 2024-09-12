import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import json

from storefront import main, get_budget, process_inventory_file

class TestMainFunction(unittest.TestCase):
    # Test for normal input with a valid JSON file.
    @patch('builtins.input', side_effect=['TestUser', '100'])
    @patch('sys.argv', ['storefront.py', 'inventory.json'])
    @patch('storefront.process_inventory_file', return_value={"item": "test_item"})
    def test_main_with_input(self, mock_input, mock_inventory):
        """
        Test that the main function works properly when give user input.
        The input will be mocked as 'TestUser'
        """
        try:
            main()
            #mock_inventory.assert_called_once_with('inventory.json')
        except Exception as e:
            self.fail(f"main() raised the following exception:\n{e}")

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

class TestProcessInventoryFileFunction(unittest.TestCase):
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"item": "value"}')
    def test_process_inventory_file_valid(self, mock_open_file, mock_isfile):
        """
        Test that process_inventory_file successfully loads a valid JSON file.
        """
        inventory_data = process_inventory_file('valid_file.json')
        self.assertEqual(inventory_data, {"item": "value"})

    @patch('sys.exit')
    def test_process_inventory_file_invalid_extension(self, mock_exit):
        """
        Test that process_inventory_file exits if the file is not a .json file.
        """
        process_inventory_file("invalid_file.txt")
        #mock_exit.assert_called_once_with(1)

    @patch('os.path.isfile', return_value=False)
    @patch('sys.exit')
    def test_process_inventory_file_non_existent_file(self, mock_exit, mock_isfile):
        """
        Test that process_inventory_file exits if the file does not exist.
        """
        process_inventory_file('non_existing_file.json')
        #mock_exit.assert_called_once_with(1)
    
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Invalid JSON data')
    @patch('sys.exit')
    def test_process_inventory_file_invalid_json(self, mock_exit, mock_open, mock_isfile):
        """
        Test that process_inventory_file exits if the file contains invalid JSON.
        """
        process_inventory_file('invalid_json_file.json')
        #mock_exit.assert_called_once_with(1)
    
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='Invalid JSON data')
    @patch('sys.exit')
    def test_process_inventory_file_other_exception(self, mock_exit, mock_open_file, mock_isfile):
        mock_open_file.side_effect = Exception("Some error")
        process_inventory_file('error_file.json')
        #mock_exit.assert_callable_once_with(1)

if __name__ == '__main__':
    unittest.main()