"""
This module contains the implementation of a shopping cart system for a PC store.

Classes:
    Cart: Represents a user's shopping cart, managing inventory and user interactions.
    
Methods in Cart:
    - default(): Handles invalid input options.
    - checkout(): Processes the purchase if the user has sufficient funds.
    - add_item(): Adds an item to the cart by its part ID.
    - add_build(): Adds a complete PC build to the cart.
    - remove_item(): Removes an item from the cart by its part ID.
    - clear_cart(): Clears the entire cart after user confirmation.
    - cart_display(): Displays the contents of the cart along with the user's name and budget.
    - cart_menu(): Manages the cart menu and user actions.
"""
import sys
from src.utils import clear_screen

class Cart:
    """
    A class representing a shopping cart for managing user-selected PC parts.

    The Cart allows users to:
    - Add individual parts or a custom PC build to the cart.
    - Remove items from the cart.
    - Display the contents and cost breakdown of the cart.
    - Clear the cart or proceed to checkout.
    
    Attributes:
        user_object (User): The user interacting with the cart.
        inventory_object (Inventory): The available parts from which the user can select.
        total_cost (int): The total cost of the items in the cart.
        build_cost (int): The total cost of a custom build, if applicable.
        cart (dict): A dictionary storing selected parts and/or a custom build.
    """
    def __init__(self, user_object, inventory_object):
        self.user_object = user_object
        self.inventory_object = inventory_object

        self.total_cost: int = 0
        self.build_cost: int = 0
        self.cart = {}

    def default(self):
        """Displays an error message for invalid input."""
        clear_screen()
        print("Not a valid option, please try again.")

    def checkout(self):
        """
        Processes the checkout if the user has sufficient funds.
        Prompts the user for confirmation before finalizing the purchase.
        """
        if self.user_object.get_budget() < self.total_cost:
            clear_screen()
            print("You don't have enough funds to purchse all of the items in your cart.")
            print("Please update your budget or remove items from the shopping cart.\n")
            return

        clear_screen()
        print("Are you sure you wish to make this purchase today?")
        user_input = input("Yes(y) / No(n): ")

        if user_input.lower() == "yes" or user_input == "y":
            clear_screen()
            print("Your purchase has been made. Thank you for choosing us for your PC needs!")
            sys.exit(0)
        else:
            return

    def add_item(self, part_id=None):
        """
        Adds an individual item to the cart by its part ID.
        
        Args:
            part_id (str, optional): The ID of the item to add. If not provided, the user is 
            prompted for input.
        """
        clear_screen()
        if part_id is None:
            print("What is the item ID of the part you want to add?")
            part_id = input("Item ID: ")
            clear_screen()

            for item in self.inventory_object.items:
                if item.id.lower() == part_id.lower():
                    self.cart[item.id] = item
                    self.total_cost = self.total_cost + item.price

    def add_build(self, build_data, build_cost):
        """
        Adds a custom PC build to the cart.

        Args:
            build_data (dict): A dictionary containing the parts of the custom build.
            build_cost (int): The total cost of the custom build.
        """
        self.build_cost = 0
        self.cart["BUILD"] = build_data
        self.build_cost += build_cost
        self.total_cost += self.build_cost

    def remove_item(self, part_id=None):
        """
        Removes an item from the cart by its part ID.
        
        Args:
            part_id (str, optional): The ID of the item to remove. If not provided, the user is 
            prompted for input.
        """
        clear_screen()
        if part_id is None:
            print("What is the item ID of the part you want to remove?")
            part_id = input("Item ID: ")

        if part_id.upper() in self.cart:
            if part_id.lower() == "build":
                self.total_cost -= self.build_cost
            else:
                item_price = self.cart[part_id.upper()].price
                item_name = self.cart[part_id.upper()].name
                self.total_cost = self.total_cost - int(item_price)
                print(f"{item_name} was successfully removed from your cart.\n")
            del self.cart[part_id.upper()]
            clear_screen()

    def clear_cart(self):
        """Clears the entire shopping cart after user confirmation."""
        clear_screen()
        print("Are you sure you wish to clear the cart. You will lose all data.")
        user_input = input("Yes/No: ")
        if user_input.lower() == 'yes' or user_input.lower() == 'y':
            self.cart = {}
            clear_screen()
        else:
            clear_screen()

    def cart_display(self):
        """Displays the contents of the cart, user details, and the total cost."""
        if not self.cart:
            print("Your cart is currently empty.")
        else:
            for item_key, item_object in self.cart.items():
                if item_key == "BUILD":
                    print("Custom PC Build")

                    print(f"    Motherboard:\n         {item_object["Motherboard"].name}"
                          f" ({item_object["Motherboard"].id.lower()}) - "
                          f"${item_object["Motherboard"].price:,}.00"
                    )

                    print(f"    CPU:\n         {item_object["CPU"].name} "
                          f"({item_object["CPU"].id.lower()}) - "
                          f"${item_object["CPU"].price:,}.00"
                    )

                    if item_object["GPU"]:
                        print(f"    GPU:\n         {item_object["GPU"].name} "
                              f"({item_object["GPU"].id.lower()}) - "
                              f"${item_object["GPU"].price:,}.00"
                    )

                    print(f"    PSU:\n         {item_object["PSU"].name} "
                          f"({item_object["PSU"].id.lower()}) - "
                          f"${item_object["PSU"].price:,}.00"
                    )

                    if item_object["RAM"]:
                        if len(item_object["RAM"]) == 1:
                            print(f"    RAM:\n         {item_object["RAM"][0].name} "
                                  f"({item_object["RAM"][0].id.lower()}) - "
                                  f"${item_object["RAM"][0].price:,}.00"
                            )
                        else:
                            print("    RAM:")
                            for dimm in item_object["RAM"]:
                                print(f"         {dimm.name} ({dimm.id.lower()}) - "
                                      f"${dimm.price:,}.00"
                                )

                    if item_object["Storage"]:
                        if len(item_object["Storage"]) == 1:
                            print(f"    Storage:\n         {item_object["Storage"][0].name} "
                                  f"({item_object["Storage"][0].id.lower()}) - "
                                  f"${item_object["Storage"][0].price:,}.00"
                            )
                        else:
                            print("    Storage:")
                            for drive in item_object["Storage"]:
                                print(f"         {drive.name} ({drive.id.lower()}) - "
                                      f"${drive.price:,}.00")
                    print("")
                else:
                    print(f"{item_object.name} ({item_object.id.lower()}) - "
                          f"${item_object.price:,}.00")
        print("--------------------------------------------------------------------------")
        print(f"Name:   {self.user_object.get_name()}")
        print(f"Budget: ${self.user_object.get_budget():,}.00")
        print("--------------------------------------------------------------------------")
        print(f"Total Cost: ${self.total_cost:,}.00")
        print("--------------------------------------------------------------------------")
        print("1. purchase item")
        print("2. remove item")
        print("3. clear cart")
        print("4. checkout")
        print("--------------------------------------------------------------------------")
        print("m. main menu")

    def cart_menu(self):
        """
        Displays the cart menu and handles user interactions like adding/removing items or 
        checkout.
        """
        clear_screen()
        while True:
            self.cart_display()
            user_input = input("\nSelect an option: ").strip().lower()

            # Break the while loop and return to the main menu
            if user_input.lower() in ('m', 'main_menu'):
                clear_screen()
                break

            menu_dict: dict = {
                "1": self.add_item,
                "2": self.remove_item,
                "3": self.clear_cart,
                "4": self.checkout
            }
            run_option = menu_dict.get(user_input, self.default)
            run_option()
