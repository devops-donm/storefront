"""
build.py

This module defines the `Build` class, which handles the creation and management of a PC build.
It allows users to add and remove components (such as CPU, GPU, RAM, PSU, etc.), check 
compatibility, and manage the total cost and power draw of the build. It also integrates 
with user, cart, and inventory objects to provide a full shopping experience.

Classes:
- Build: Manages the user's build, including adding/removing items, checking compatibility, 
  adjusting cost/power, and interfacing with the shopping cart.

Functions:
- add_item: Adds an item to the build.
- remove_item: Removes an item from the build.
- clear_build: Clears the entire build.
- add_to_cart: Adds the build to the cart if it passes compatibility checks.
- display_build_list: Displays the current list of items in the build.
- build_display: Displays build details and menu options.
- build_menu: Displays and handles the build menu.

Acknowledged Pylint Standard Errors:
src\\build.py:23:0: E0401: Unable to import 'src.utils' (import-error)
src\\build.py:309:31: E1101: Instance of 'list' has no 'name' member (no-member)
src\\build.py:309:51: E1101: Instance of 'list' has no 'id' member (no-member)
src\\build.py:310:28: E1101: Instance of 'list' has no 'price' member (no-member)
"""
# pylint: disable=R0801
from src.utils import clear_screen # pylint: disable=import-error

class Build:
    """
    Manages the creation and modification of a PC build for the user.

    This class allows users to add or remove components (CPU, GPU, RAM, etc.) 
    to/from a build, check compatibility, track the total cost and power draw, 
    and manage interactions with the shopping cart and user inventory.

    Attributes:
        user_object: The user associated with the build.
        cart_object: The shopping cart for storing completed builds.
        inventory_object: The inventory of available parts.
        compatibility_object: Handles compatibility checks for the build.
        total_cost (int): The total cost of the build.
        total_power_draw (int): The total power draw of the build.
        build (dict): Dictionary holding the components of the build.

    Methods:
        add_item(part_id): Adds an item to the build, updating cost and power draw.
        remove_item(): Removes an item from the build, updating cost and power draw.
        clear_build(): Resets the build, clearing all components and data.
        add_to_cart(): Adds the current build to the shopping cart if it's compatible.
        display_build_list(): Displays the list of current items in the build.
        build_display(): Displays details of the build along with menu options.
        build_menu(): Provides a menu for interacting with the build.
    """

    def __init__(self, user_object, cart_object, inventory_object, compatibility_object):
        self.user_object = user_object
        self.cart_object = cart_object
        self.inventory_object = inventory_object
        self.compatibility_object = compatibility_object

        self.total_cost: int = 0
        self.total_power_draw: int = 0
        self.build = {
                    "CPU": None,
                    "GPU": None,
                    "RAM": [],
                    "PSU": None,
                    "Motherboard": None,
                    "Storage": []
                    }

    def default(self):
        """
        Handle invalid options by prompting the user to try again.
        """
        print("Not a valid option, please try again.")

    def increase_total_cost(self, amount):
        """
        Increase the total cost by a specified amount.

        Args:
            amount (int): The amount to add to the total cost.
        """
        self.total_cost += amount

    def decrease_total_cost(self, amount):
        """
        Decrease the total cost by a specified amount.

        Args:
            amount (int): The amount to subtract from the total cost.
        """
        self.total_cost -= amount

    def increase_available_power(self, wattage):
        """
        Increase the total power draw by a specified wattage.

        Args:
            wattage (int): The amount of power (in watts) to add to the total power draw.
        """
        self.total_power_draw += wattage

    def decreate_available_power(self, wattage):
        """
        Decrease the total power draw by a specified wattage.

        Args:
            wattage (int): The amount of power (in watts) to subtract to the total power draw.
        """
        self.total_power_draw -= wattage

    def add_item(self, part_id=None):
        """
        Add an item to the build based on its part ID. If no part ID is provided,
        prompts the user for input and searches the inventory for a matching item.

        Args:
            part_id (str, optional): The ID of the part to add. If None, the method
            will prompt the user to input a part ID.
        
        The method updates the build with the part, adjusts the total cost, and updates
        power draw or supplied power based on the type of item (RAM, Storage, PSU, etc.).
        """
        clear_screen()
        if part_id is None:
            print("What is the part ID of the item you want to add?")
            part_id = input("Item ID: ")
            clear_screen()

            for item in self.inventory_object.items:
                if item.id.lower() == part_id.lower():
                    if item.type.lower() == "ram":
                        self.build["RAM"].append(item)
                    elif item.type.lower() == "storage":
                        self.build["Storage"].append(item)
                    else:
                        self.build[item.type] = item

                    self.increase_total_cost(item.price)

                    if item.type != "PSU":
                        self.decreate_available_power(item.power_draw)
                    else:
                        self.increase_available_power(item.power_supplied)

    def ram_storage_removal(self, item):
        """
        Remove a RAM or Storage item from the build.

        This method handles the removal of items from build components that allow 
        multiple entries, such as RAM or storage. It checks the current quantity of 
        items and proceeds with one of the following actions:
        
        - If no items are present, it displays a message that nothing can be deleted.
        - If exactly one item is present, it removes that item from the build.
        - If more than one item is present, the user is prompted to input the 
        Part ID of the item they wish to remove, and that item is removed.

        Args:
            item: The item to be removed from the build (either RAM or storage).
        """
        if len(self.build[item.type]) == 0:
            self.build[item.type] = []
            clear_screen()
            print(f"Nothing in {item.type} to delete.")
        elif len(self.build[item.type]) == 1:
            self.build[item.type] = []
            self.decrease_total_cost(item.price)
            self.increase_available_power(item.power_draw)
            clear_screen()
        elif len(self.build[item.type]) > 1:
            clear_screen()
            user_input = input(f"What is the {item.type} Part ID: ")
            for ram_object in self.build[item.type]:
                if ram_object.id.lower() == user_input.lower():
                    self.build[item.type].remove(ram_object)
                    self.decrease_total_cost(item.price)
                    self.increase_available_power(item.power_draw)
                    break

    def psu_removal(self, item):
        """
        Removes the PSU from the build, updates the total cost, and decreases the available 
        power capacity.
        """
        self.build[item.type] = None
        self.decrease_total_cost(item.price)
        self.decreate_available_power(item.power_capacity)
        clear_screen()

    def remove_item(self):
        """
        Remove an item from the build based on its part type. Prompts the user to input
        the part type and optionally a specific part ID if multiple items of that type exist.

        The method adjusts the build by removing the part, clears the item from the build,
        and prompts the user when no items are available to delete.

        After removing the item, future steps will need to adjust the total cost and power
        draw or supplied power.
        """
        clear_screen()
        print("What is the part type of the item you want to remove?")
        part = input("Part Type: ")

        for item in self.inventory_object.items:
            if item.type.lower() == part.lower():
                if item.type.lower() == "ram" or item.type.lower() == "storage":
                    self.ram_storage_removal(item)
                    print(f"Item has been removed from {item.type}.")
                elif item.type.lower() == "psu":
                    self.psu_removal(item)
                    print(f"Item has been removed from {item.type}.")
                else:
                    self.build[item.type] = None
                    clear_screen()
                    print(f"{item.name} ({item.id}) was removed from build.\n")

    def clear_build(self):
        """
        Clear the current build after user confirmation.

        Prompts the user for confirmation before resetting the build. If confirmed, 
        it resets the build dictionary to default values (None for single components 
        like CPU, GPU, PSU, etc., and empty lists for RAM and Storage), sets the 
        total cost and total power draw to 0.

        If the user chooses not to reset, the build remains unchanged.

        The function clears the screen before and after important prompts.
        """
        clear_screen()
        print("Are you sure you wish to clear the current build? You will lose all data.")
        user_input = input("Yes/No: ")
        if user_input.lower() == "yes" or user_input.lower() == 'y':
            clear_screen()
            self.build = {
                    "CPU": None,
                    "GPU": None,
                    "RAM": [],
                    "PSU": None,
                    "Motherboard": None,
                    "Storage": []
                    }
            self.total_cost = 0
            self.total_power_draw = 0
            print("Build has successfully been reset.")
        else:
            clear_screen()
            print("Build did not get reset.")

    def add_to_cart(self):
        """
        Add the current build to the shopping cart if it passes the compatibility check.

        The method performs a compatibility test on the current build using the 
        `compatibility_object`. If the build passes the test, it adds the build 
        and its total cost to the cart using the `cart_object` and notifies the user 
        that the build has been successfully added.

        If the build is not compatible, the method alerts the user and suggests reviewing 
        the compatibility check for more details.

        This method clears the screen before displaying messages.
        """
        compatibility_test = self.compatibility_object.build_check(
            self.build, self.total_power_draw
        )
        if compatibility_test:
            self.cart_object.add_build(self.build, self.total_cost)
            clear_screen()
            print("Build has been added to the shopping cart!")
        else:
            clear_screen()
            print("Build is not compatible. See Build - Compatibility Check for more information.")

    def display_build_list(self):
        """
        Display the current build components and their details.

        This method iterates through the build dictionary and prints out the name, 
        ID, and price of each component. For components that allow multiple entries 
        (such as RAM and Storage), it lists each item in the respective category. 
        If a component is missing from the build, it displays 'None' for that component.

        Note:
            - RAM and Storage are handled separately as they can have multiple items.

        This method provides a summary of the build in a readable format with proper 
        formatting of the prices (using commas).
        """
        for item_key, item_object in self.build.items():
            if not item_object:
                print(f"{item_key.upper()}: None")

            else:
                if item_key == "RAM":
                    print("RAM:")
                    for dimm in item_object:
                        print(f"    {dimm.name} ({dimm.id.lower()}) - ${dimm.price:,}.00")

                elif item_key == "Storage":
                    print("Storage:")
                    for drive in item_object:
                        print(f"    {drive.name} ({drive.id.lower()}) - ${drive.price:,}.00")

                else:
                    print(f"{item_key.upper()}:")
                    print(
                        f"    {item_object.name} ({item_object.id.lower()}) - " # pylint: disable=no-member
                        f"${item_object.price:,}.00" # pylint: disable=no-member
                    )

    def build_display(self):
        """
        Display the current build overview and options for managing the build.

        This method prints out a formatted display of the current user's name, 
        budget, total cost of the build, and the total power draw in watts. 
        It also presents a menu of options that the user can choose from, including 
        adding or removing items, checking compatibility, clearing the build, or 
        adding the build to the cart.

        The display includes section separators for readability and a prompt to 
        return to the main menu by pressing 'm'.
        """
        print("--------------------------------------------------------------------------")
        print(f"Name:   {self.user_object.get_name()}")
        print(f"Budget: ${self.user_object.get_budget():,}.00")
        print("--------------------------------------------------------------------------")
        print(f"Total Cost: ${self.total_cost:,}.00")
        print(f"Power Draw: {self.total_power_draw}W")
        print("--------------------------------------------------------------------------")
        print("1. add item")
        print("2. remove item")
        print("3. check compatibility")
        print("4. clear build")
        print("5. add build to cart")
        print("--------------------------------------------------------------------------")
        print("m: Main Menu")

    def build_menu(self):
        """
        Display the build menu and handle user input to manage the current build.

        This method clears the screen, then enters a loop to continuously display 
        the current build list and build menu options. The user can select from 
        a variety of options, such as adding an item, removing an item, checking 
        build compatibility, clearing the build, or adding the build to the cart.

        The user can input 'm' or 'main_menu' to return to the main menu, 
        which breaks the loop.

        The menu options are mapped to their corresponding functions using 
        a dictionary (`menu_dict`), and the selected option is executed based 
        on user input. If the input is invalid, the default method is called.
        """
        clear_screen()
        while True:
            self.display_build_list()

            self.build_display()
            user_input = input("\nSelect an option: ").strip().lower()

            # Break the while loop and return to the main menu
            if user_input.lower() in ('m', 'main_menu'):
                clear_screen()
                break

            menu_dict: dict = {
                "1": self.add_item,
                "2": self.remove_item,
                "3": lambda: self.compatibility_object.build_check(
                    self.build, self.total_power_draw
                ),
                "4": self.clear_build,
                "5": self.add_to_cart
            }
            run_option = menu_dict.get(user_input, self.default)
            run_option()
