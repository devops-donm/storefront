from src.utils import clear_screen
from typing import List, Union

class Item:
    def __init__(self, id: str, type: str, name: str, price: float, power_draw: float = 0):
        self.id = id
        self.type = type
        self.name = name
        self.price = price
        self.power_draw = power_draw
    
    def __str__(self) -> str:
        return f"{self.name} ({self.type}) - ${self.price}"

class CPU(Item):
    def __init__(self, id: str, name: str, price: float, power_draw: float, socket: str):
        super().__init__(id, "CPU", name, price, power_draw)
        self.socket = socket

class GPU(Item):
    def __init__(self, id: str, name: str, price: float, power_draw: float, overclockable: bool):
        super().__init__(id, "GPU", name, price, power_draw)
        self.overclockable = overclockable

class RAM(Item):
    def __init__(self, id: str, name: str, price: float, power_draw: float, capacity: int):
        super().__init__(id, "RAM", name, price, power_draw)
        self.capactiy = capacity

class PSU(Item):
    def __init__(self, id: str, name: str, price: float, power_supplied: float):
        super().__init__(id, "PSU", name, price)
        self.power_supplied = power_supplied

class Motherboard(Item):
    def __init__(self, id: str, name: str, price: float, power_draw: float, socket: str, ram_slots: int):
        super().__init__(id, "Motherboard", name, price, power_draw)
        self.socket = socket
        self.ram_slots = ram_slots

class Storage(Item):
    def __init__(self, id: str, name: str, price: float, capacity: int):
        super().__init__(id, "Storage", name, price)
        self.capacity = capacity

class Inventory:
    def __init__(self) -> None:
        self.items: List[Item] = []
    
    def add_item(self, item: Item):
        self.items.append(item)

def load_inventory(data: dict) -> Inventory:
    inventory = Inventory()
    for entry in data["inventory"]:
        item_data = entry["item"]
        item_type = item_data["type"]

        if item_type == "CPU":
            item = CPU(
                id = item_data["id"],
                name = item_data["name"],
                price = item_data["price"],
                power_draw = item_data["power_draw"],
                socket = item_data["socket"]
            )
        elif item_type == "GPU":
            item = GPU(
                id = item_data["id"],
                name = item_data["name"],
                price = item_data["price"],
                power_draw = item_data["power_draw"],
                overclockable = item_data["overclockable"]
            )
        elif item_type == "RAM":
            item = RAM(
                id = item_data["id"],
                name = item_data["name"],
                price = item_data["price"],
                power_draw = item_data["power_draw"],
                capacity = item_data["capacity"]
            )
        elif item_type == "PSU":
            item = PSU(
                id = item_data["id"],
                name = item_data["name"],
                price = item_data["price"],
                power_supplied = item_data["power_supplied"]
            )
        elif item_type == "Motherboard":
            item = Motherboard(
                id = item_data["id"],
                name = item_data["name"],
                price = item_data["price"],
                power_draw = item_data["power_draw"],
                socket = item_data["socket"],
                ram_slots = item_data["ram_slots"]
            )
        elif item_type == "Storage":
            item = Storage(
                id = item_data["id"],
                name = item_data["name"],
                price = item_data["price"],
                capacity = item_data["capacity"]
            )

        inventory.add_item(item)

    return inventory



available_category_options = [
                                    "all",
                                    "cpu",
                                    "gpu",
                                    "ram",
                                    "psu",
                                    "motherboard",
                                    "storage"
                                ]
def print_categories():
    for category in available_category_options:
        print(category)

def list_parts(inventory_data):
    """
    Fuction to list parts from inventory based on user-specified category.
    """
    clear_screen()
    print_categories()
    print("\nFrom the provided categories what would you like to list? ")
    user_input = input("Option: ").lower()

    if user_input == 'all':
        clear_screen()
        for item in inventory_data.items:
            print(item)
    else:
        for item in inventory_data.items:
            if item.type.lower() == user_input.lower():
                print(item)

def get_details(inventory_data, part_id=None):
    part_details = None
    
    if part_id is None:
        print("\nBy the Part ID what part would you like the details for? ")
        print("'m' for Main Menu")
        user_input = input("Option: ").lower()

        clear_screen()
        if user_input == 'm':
            return
        
        for item in inventory_data.items:
            if item.id.lower() == user_input.lower():
                #for attr, value in vars(item).items():
                part_details = item
            
        for attr, value in vars(part_details).items():
            print(f"{attr}: {value}")
        
    else:
        #TODO: If part_id is provided, directly find the part.
        for item in inventory_data.items:
            if item.id.lower() == part_id.lower():
                return item
            else:
                return None