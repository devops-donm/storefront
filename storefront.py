import sys
import os
import json

from src.utils import clear_screen

def get_budget():
    """
    Prompt the user to enter their budget.

    Returns:
        int: The user's budget.
    """
    while True:
        try:
            budget = int(input("What is your budget? "))
            if budget <= 0:
                raise ValueError("Budget must be a positive amount.")
            else:
                return budget
        except ValueError as e:
            print(f"Invalid input. {e} Please enter a valid positive integer.")

def process_inventory_file(inventory_file):
    # Check if the file has a .json extension
    if not inventory_file.endswith('.json'):
        print("Error: File must be a .json file.")
        sys.exit(1)

    # Check if the file exists
    if not os.path.isfile(inventory_file):
        print(f"Error: The file '{inventory_file}' does not exist.")
        sys.exit(1)

    # Load the JSON data
    try:
        with open(inventory_file, 'r') as file:
            inventory_data = json.load(file)
            return inventory_data
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON.\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unable to load the file.\n{e}")
        sys.exit(1)

def main():
    """
    Main function to run the application.
    """

    if len(sys.argv) != 2:
        print("\nUsage: python3 storefront.py inventory.json")
        print("Or you can make storefront.py an exicutable and run ./storefront.py inventory.json\n")
        sys.exit(1)
    
    inventory_file = sys.argv[1]
    inventory_data = process_inventory_file(inventory_file)

    user_name = input("What is your name? ")
    budget = get_budget()
    clear_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("Goodbye")