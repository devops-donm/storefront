"""
This module defines classes and functions to manage an inventory system for computer parts. 

Classes:
    - Item: Base class representing an item with common attributes such as item_id, 
      item_type, name, price, and power_draw.
    - CPU: Represents a CPU, extending Item, with an additional socket attribute.
    - GPU: Represents a GPU, extending Item, with an additional overclockable attribute.
    - RAM: Represents RAM, extending Item, with an additional capacity attribute.
    - PSU: Represents a power supply unit, extending Item, with an additional power_supplied 
      attribute.
    - Motherboard: Represents a motherboard, extending Item, with additional socket and 
      ram_slots attributes.
    - Storage: Represents storage devices, extending Item, with an additional capacity attribute.
    - Inventory: Manages a collection of items, providing functionality to add items.

Functions:
    - load_inventory: Loads inventory data from a dictionary and populates it with items based 
      on their types.
    - print_categories: Prints a list of available item categories.
    - gen_parts_dict: Generates a dictionary categorizing parts by their type.
    - list_parts: Lists all parts or parts from a specific category based on user input.
    - get_part_details: Retrieves details of a specific part by its item ID.
    - display_part_details: Displays detailed information about a specific part.
    - get_details: Fetches and displays part details, optionally based on user input.
"""

from typing import List
from src.utils import clear_screen # pylint: disable=import-error

class Item: # pylint: disable=too-few-public-methods
    """
    Represents a base class for computer parts in the inventory.

    Attributes:
        - item_id (str): A unique identifier for the item.
        - item_type (str): The type of the item (e.g., CPU, GPU, RAM, etc.).
        - name (str): The name of the item.
        - price (int): The price of the item in dollars.
        - power_draw (int): The amount of power (in watts) the item draws. Default is 0.
        
    Methods:
        - __str__: Returns a string representation of the item, including its name, type, 
        and price.
    """
    def __init__(self, item_id: str, item_type: str, name: str, price: int, power_draw: int = 0): # pylint: disable=too-many-positional-arguments, too-many-arguments
        self.item_id = item_id
        self.item_type = item_type
        self.name = name
        self.price = price
        self.power_draw = power_draw

    def __str__(self) -> str:
        return f"{self.name} ({self.item_type}) - ${self.price}"

class CPU(Item): # pylint: disable=too-few-public-methods
    """
    Represents a CPU in the inventory.

    Attributes:
        socket (str): The CPU socket type.
    """
    def __init__(self, item_id: str, name: str, price: int, power_draw: int, socket: str): # pylint: disable=too-many-positional-arguments, too-many-arguments
        super().__init__(item_id, "CPU", name, price, power_draw)
        self.socket = socket

class GPU(Item): # pylint: disable=too-few-public-methods
    """
    Represents a GPU in the inventory.

    Attributes:
        overclockable (bool): If the GPU can be overclocked.
    """
    def __init__(self, item_id: str, name: str, price: int, power_draw: int, overclockable: bool): # pylint: disable=too-many-positional-arguments, too-many-arguments
        super().__init__(item_id, "GPU", name, price, power_draw)
        self.overclockable = overclockable

class RAM(Item): # pylint: disable=too-few-public-methods
    """
    Represents a RAM in the inventory.

    Attributes:
        capacity (int): Determines the total amount of memory.
    """
    def __init__(self, item_id: str, name: str, price: int, power_draw: int, capacity: int): # pylint: disable=too-many-positional-arguments, too-many-arguments
        super().__init__(item_id, "RAM", name, price, power_draw)
        self.capacity = capacity

class PSU(Item): # pylint: disable=too-few-public-methods
    """
    Represents a PSU in the inventory.

    Attributes:
        power_supplied (int): Total provided power supplied to the computer.
    """
    def __init__(self, item_id: str, name: str, price: int, power_supplied: int): # pylint: disable=too-many-positional-arguments, too-many-arguments
        super().__init__(item_id, "PSU", name, price)
        self.power_supplied = power_supplied

class Motherboard(Item): # pylint: disable=too-few-public-methods
    """
    Represents a GPU in the inventory.

    Attributes:
        socket (str): The Motherboard socket type.
        ram_slots (int): Total amount of RAM the Motherboard can support.
    """
    def __init__(self, item_id: str, name: str, price: int, power_draw: int, # pylint: disable=too-many-positional-arguments, too-many-arguments
                 socket: str, ram_slots: int):  # pylint: disable=too-many-positional-arguments, too-many-arguments
        super().__init__(item_id, "Motherboard", name, price, power_draw)
        self.socket = socket
        self.ram_slots = ram_slots

class Storage(Item): # pylint: disable=too-few-public-methods
    """
    Represents a Storage in the inventory.

    Attributes:
        capacity (int): Determines the total amount of storage.
    """
    def __init__(self, item_id: str, name: str, price: int, capacity: int): # pylint: disable=too-many-positional-arguments
        super().__init__(item_id, "Storage", name, price)
        self.capacity = capacity

class Inventory: # pylint: disable=too-few-public-methods
    """
    Represents an inventory of items.
    
    Attributes:
        items (List[Item]): A list to store the items in the inventory.
    """
    def __init__(self) -> None:
        self.items: List[Item] = []

    def add_item(self, item: Item):
        """
        Adds an item to the inventory.

        Args:
            item (Item): The item to be added to the inventory.
        """
        self.items.append(item)

def load_inventory(data: dict) -> Inventory:
    """
    Loads the inventory from a dictionary containing item data.

    Args:
        data (dict): The data containing inventory details.

    Returns:
        Inventory: The inventory object populated with items.
    """
    inventory = Inventory()
    for entry in data["inventory"]:
        item_data = entry["item"]
        item_type = item_data["type"]

        if item_type == "CPU":
            item = CPU(
                item_id=item_data["id"],
                name=item_data["name"],
                price=item_data["price"],
                power_draw=item_data["power_draw"],
                socket=item_data["socket"]
            )
        elif item_type == "GPU":
            item = GPU(
                item_id=item_data["id"],
                name=item_data["name"],
                price=item_data["price"],
                power_draw=item_data["power_draw"],
                overclockable=item_data["overclockable"]
            )
        elif item_type == "RAM":
            item = RAM(
                item_id=item_data["id"],
                name=item_data["name"],
                price=item_data["price"],
                power_draw=item_data["power_draw"],
                capacity=item_data["capacity"]
            )
        elif item_type == "PSU":
            item = PSU(
                item_id=item_data["id"],
                name=item_data["name"],
                price=item_data["price"],
                power_supplied=item_data["power_supplied"]
            )
        elif item_type == "Motherboard":
            item = Motherboard(
                item_id=item_data["id"],
                name=item_data["name"],
                price=item_data["price"],
                power_draw=item_data["power_draw"],
                socket=item_data["socket"],
                ram_slots=item_data["ram_slots"]
            )
        elif item_type == "Storage":
            item = Storage(
                item_id=item_data["id"],
                name=item_data["name"],
                price=item_data["price"],
                capacity=item_data["capacity"]
            )

        inventory.add_item(item) # pylint: disable=possibly-used-before-assignment

    return inventory

available_category_options = [
    "all", "cpu", "gpu", "ram", "psu", "motherboard", "storage"
]

def print_categories():
    """
    Prints the available categories.

    Args:
        categories (list): A list of category names to print. 
        Defaults to available_category_options.
    """
    for category in available_category_options:
        print(category)

def gen_parts_dict(inventory_data):
    """
    Generates a dictionary that categorizes parts in the inventory by their type.

    Args:
        inventory_data (object): An object containing a list of parts (items) 
        in the inventory, where each item has attributes such as `item_type`.

    Returns:
        dict: A dictionary where the keys are part types (e.g., "cpu", "gpu", etc.)
        and the values are lists of items corresponding to each part type.
    """
    parts_dict = {
        "cpu": [],
        "gpu": [],
        "ram": [],
        "psu": [],
        "motherboard": [],
        "storage": []
    }

    for item in inventory_data.items:
        parts_dict[item.item_type.lower()].append(item)
    return parts_dict

def list_parts(inventory_data):
    """
    Displays a list of parts from the inventory based on user selection.

    Args:
        inventory_data (object): An object containing the inventory, which 
        holds the list of parts and their details.

    The function:
    1. Clears the screen.
    2. Generates a dictionary of parts categorized by type.
    3. Prompts the user to select a category or list all parts.
    4. Displays parts in the selected category or all parts if 'all' is chosen.
    """
    clear_screen()
    parts_dictionary = gen_parts_dict(inventory_data)
    print_categories()
    print("\nFrom the provided categories what would you like to list? ")
    user_input = input("Option: ").lower()

    if user_input == 'all':
        clear_screen()
        for part_key in parts_dictionary:
            print(part_key.upper())
            parts_list = parts_dictionary.get(part_key)
            for part_item in parts_list:
                print(f"    {part_item.name} ({part_item.item_id.lower()})    \
                      ${part_item.price:,}.00")
    elif user_input in parts_dictionary:
        clear_screen()
        print(user_input.upper())
        parts_list = parts_dictionary.get(user_input)
        for part_item in parts_list:
            print(f"    {part_item.name} ({part_item.item_id.lower()})    \
                  ${part_item.price:,}.00")

def get_part_details(inventory_data, user_input):
    """
    Retrieves the part details from the inventory based on the user's input.

    Args:
        inventory_data (object): An object containing a list of items in the inventory.
        user_input (str): The ID of the part that the user wants to look up.
    
    Returns:
        object: The item from the inventory that matches the user's input (by `item_id`), 
        or `None` if no match is found.
    """
    for item in inventory_data.items:
        if item.item_id.lower() == user_input.lower():
            return item
    return None

def display_part_details(part_details):
    """
    Displays detailed information about a computer part.

    Args:
        part_details (object): An object containing attributes about the part,
        such as 'name', 'price', 'item_id', 'item_type', and potentially other
        attributes like 'power_draw' or 'power_supplied' depending on the part type.

    The function will print the part's name, ID, type, price, and power information.
    It also prints any other available attributes that aren't excluded in the 
    'other_attr' list.
    """
    part_name = part_details.name
    part_price = part_details.price
    part_id = part_details.item_id
    part_type = part_details.item_type
    part_power = None
    other_attr = []

    for attr, value in vars(part_details).items():
        if attr == 'item_type':
            part_power = part_details.power_draw if value != "PSU" else part_details.power_supplied
        if attr not in ('name', 'price', 'item_id', 'item_type', 'power_draw', 'power_supply'):
            other_attr.append({attr: value})

    print(f"{part_name} ({part_id.lower()})")
    print(f"\tType: {part_type}")
    print(f"\tPrice: ${part_price:,}.00")
    print(f"\tPower: {part_power}W")

    for other_attr_data in other_attr:
        for attr, value in other_attr_data.items():
            print(f"\t{attr}: {value}")

def get_details(inventory_data, part_id=None):
    """
    Fetches and displays part details based on the provided part ID.

    If no part ID is provided, it prompts the user for input.

    Args:
        inventory_data (dict): The inventory data containing all parts.
        part_id (str, optional): The part ID to look up. If None, user input is requested.

    Returns:
        dict or None: The details of the part, or None if not found or user returns to the 
        main menu.
    """
    if part_id is None:
        clear_screen()
        print("\nBy the Part ID what part would you like the details for? ")
        print("'m' for Main Menu")
        user_input = input("Option: ").lower()

        clear_screen()
        if user_input == 'm':
            return None

        part_details = get_part_details(inventory_data, user_input)

        if part_details is None:
            return None

        display_part_details(part_details)
        return part_details

    part_details = get_part_details(inventory_data, part_id)
    return part_details
