"""
menu.py
Menu system for storefront.py
"""
import sys

from src.utils import clear_screen
from src.inventory import Inventory

def default():
    print("Not a valid option, please try again.")

def help_option():
    print("""
          - Select from the available options to perform an action.\n
          - You can choose to either select individual parts to add to\n
          your shopping cart or build a custom PC.\n
          - You can also check the compatibility of parts for a custom PC\n
          build.\n
          - Please open an issue ticket on our github page for bugs or\n
          new features.\n
          - Please review our README before contacting support. Thank you!
          """)

def exit_program():
    clear_screen()
    print("Thank you and Goodbye!")
    sys.exit(0)

def display_menu(user_name, budget):
    print("--------------------------------------------------------------------------")
    print(user_name)
    print(f"${budget}.00")
    print("--------------------------------------------------------------------------")
    print("1. list (L)")
    print("--------------------------------------------------------------------------")
    print("H) Help    E) Exit")

def main_menu(user_name, budget, inventory_data):
    while True:
        inventory_object = Inventory(inventory_data)

        display_menu(user_name, budget)
        user_input = input("\nSelect an option: ").strip().lower()

        # Dictionary of available command options
        menu_dict: dict = {
            "list": lambda: inventory_object.list_parts(),
            "l": lambda: inventory_object.list_parts(),
            "help": help_option,
            "h": help_option,
            "exit": exit_program,
            "e": exit_program,
        }

        clear_screen()
        run_option = menu_dict.get(user_input, default)
        run_option()