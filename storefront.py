"""
storefront.py

This module serves as the entry point for a storefront application that processes an inventory 
file and displays a user menu to interact with the inventory.

The application expects a JSON file containing inventory data, which it processes to allow 
users to interact with the store's inventory. The primary functionalities of this module 
include validating the input file, loading and processing the inventory data, and initiating 
the main menu for user interaction.

Functions:
- process_inventory_file(inventory_file): Validates and loads the JSON inventory file, 
  ensuring it exists and is in the correct format.
- main(): The main function that acts as the application's entry point, handling the initial
  setup and triggering the user interface.

Usage:
To run the application:
    python3 storefront.py <inventory_file.json>
"""

import json
import sys

from src.inventory import load_inventory # pylint: disable=import-error
from src.menu import main_menu # pylint: disable=import-error
from src.utils import clear_screen # pylint: disable=import-error

def process_inventory_file(inventory_file):
    """
    Validates and loads inventory data from a JSON file.

    Args:
        inventory_file (str): Path to the JSON file containing the inventory data.

    Returns:
        dict: Loaded inventory data if the file is valid and successfully processed.

    Exits:
        On file format, existence, or decoding errors, the program will terminate.
    """

    # Check if the file has a .json extension
    if not inventory_file.endswith('.json'):
        print("Error: File must be a .json file.")
        sys.exit(1)

    # Load the JSON data
    try:
        with open(inventory_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            inventory_data = load_inventory(json_data)
            return inventory_data
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON.\n{e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: The file {inventory_file} was not found.\n{e}")
        sys.exit(1)
    except OSError as e:
        print(f"Error: There was an issue opening the file.\n{e}")
        sys.exit(1)

def main():
    """
    Main function to run the application.
    """

    if len(sys.argv) != 2:
        print("\nUsage: python3 storefront.py inventory.json")
        print("Or you can make storefront.py an exicutable and run \
              ./storefront.py inventory.json\n")
        sys.exit(1)

    inventory_file = sys.argv[1]
    inventory_data = process_inventory_file(inventory_file)

    main_menu(inventory_data)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("Goodbye")
