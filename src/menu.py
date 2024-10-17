"""
menu.py
Menu system for storefront.py
"""
import sys

from src.utils import clear_screen
from src.inventory import list_parts, get_details
from src.compatibility import Compatibility
from src.build import Build
from src.cart import Cart
from src.user import User

def default():
    print("Not a valid option, please try again.")

def help_option():
    print("""
          - list: Get a list of parts by category.
          - details: Get the details of an individial item by providing the item ID.
          - compatibility: Check the compatibility of two or more parts.
          - build: Select parts to create your own custom PC.
          - compatibility_build: Verify that all the parts in your build are compatible.
          - remove: Remove a part or build from your shopping cart.
          - purchase: Purchase the item(s) in your shopping cart.
          - cart: View and edit the items in your shopping cart.
          - checkout: Final review of the items from your cart leading to the final purchase.
          - budget: Edit your budget. USD, Whole Numbers Only.
          """)

def exit_program():
    clear_screen()
    print("Thank you and Goodbye!")
    sys.exit(0)

def display_menu(user_name, budget):
    print("--------------------------------------------------------------------------")
    print(f"Name:   {user_name}")
    print(f"Budget: ${budget:,}.00")
    print("--------------------------------------------------------------------------")
    print("1.  list")
    print("2.  details")
    print("3.  compatibility")
    print("4.  build")
    print("5.  cart")
    print("6.  change budget")
    print("7.  change name")
    print("--------------------------------------------------------------------------")
    print("11. Help    12. Exit")

def main_menu(inventory_data):

    #TODO: Move this initial logic over to storefront.py and add to function arg.
    user_object = User()
    user_object.update_name()
    user_object.update_budget()
    clear_screen()

    compatibility_object = Compatibility(inventory_data)
    cart_object = Cart(user_object, inventory_data)
    build_object = Build(user_object, cart_object, inventory_data, compatibility_object)
    
    while True:
        display_menu(user_object.get_name(), user_object.get_budget())
        user_input = input("\nSelect an option: ").strip().lower()

        # Dictionary of available command options
        menu_dict: dict = {
            "1": lambda: list_parts(inventory_data),
            "list": lambda: list_parts(inventory_data),
            
            "2": lambda: get_details(inventory_data),
            "detail": lambda: get_details(inventory_data),
            
            "3": compatibility_object.compatibility_check,
            "compatibility": compatibility_object.compatibility_check,

            "4": build_object.build_menu,
            "build": build_object.build_menu,

            "5": cart_object.cart_menu,
            "cart": cart_object.cart_menu,

            "6": user_object.update_budget,
            "budget": user_object.update_budget,

            "7": user_object.update_name,
            "user": user_object.update_name,
            "username": user_object.update_name,

            "11": help_option,
            "help": help_option,
            "h": help_option,
            
            "12": exit_program,
            "exit": exit_program,
            "e": exit_program,
        }

        run_option = menu_dict.get(user_input, default)
        run_option()