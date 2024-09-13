"""
menu.py
Menu system for storefront.py
"""
import sys

from src.utils import clear_screen

def default():
    print("Not a valid option, please try again.")

def exit_program():
    clear_screen()
    print("Thank you and Goodbye!")
    sys.exit(0)

def display_menu(user_name, budget):
    print("--------------------------------------------------------------------------")
    print(user_name)
    print(f"${budget}.00")
    print("--------------------------------------------------------------------------")
    print("Options Placeholder")
    print("--------------------------------------------------------------------------")
    print("E) Exit")

def main_menu(user_name, budget, inventory_data):
    while True:
        display_menu(user_name, budget)
        user_input = input("\nSelect an option: ").strip().lower()

        # Dictionary of available command options
        menu_dict: dict = {
            "e": exit_program,   
        }

        clear_screen()
        run_option = menu_dict.get(user_input, default)
        run_option()