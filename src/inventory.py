from src.utils import clear_screen
from typing import List

class Item:
    def __init__(self, id: str, type: str, name: str, price: int, power_draw: int = 0):
        self.id = id
        self.type = type
        self.name = name
        self.price = price
        self.power_draw = power_draw

    def __str__(self) -> str:
        return f"{self.name} ({self.type}) - ${self.price}"

class CPU(Item):
    def __init__(self, id: str, name: str, price: int, power_draw: float, socket: str):
        super().__init__(id, "CPU", name, price, power_draw)
        self.socket = socket

class GPU(Item):
    def __init__(self, id: str, name: str, price: int, power_draw: float, overclockable: bool):
        super().__init__(id, "GPU", name, price, power_draw)
        self.overclockable = overclockable

class RAM(Item):
    def __init__(self, id: str, name: str, price: int, power_draw: float, capacity: int):
        super().__init__(id, "RAM", name, price, power_draw)
        self.capactiy = capacity

class PSU(Item):
    def __init__(self, id: str, name: str, price: int, power_supplied: float):
        super().__init__(id, "PSU", name, price)
        self.power_supplied = power_supplied

class Motherboard(Item):
    def __init__(self, id: str, name: str, price: int, power_draw: float,
                 socket: str, ram_slots: int):
        super().__init__(id, "Motherboard", name, price, power_draw)
        self.socket = socket
        self.ram_slots = ram_slots

class Storage(Item):
    def __init__(self, id: str, name: str, price: int, capacity: int):
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

def gen_parts_dict(inventory_data):
    parts_dict = {
            "cpu": [],
            "gpu": [],
            "ram": [],
            "psu": [],
            "motherboard": [],
            "storage": []
        }

    for item in inventory_data.items:
        parts_dict[item.type.lower()].append(item)
    return parts_dict

def list_parts(inventory_data):
    """
    Fuction to list parts from inventory based on user-specified category.
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
                print(f"    {part_item.name} ({part_item.id.lower()})    ${part_item.price:,}.00")
    elif user_input in parts_dictionary:
        clear_screen()
        print(user_input.upper())
        parts_list = parts_dictionary.get(user_input)
        for part_item in parts_list:
            print(f"    {part_item.name} ({part_item.id.lower()})    ${part_item.price:,}.00")

def get_details(inventory_data, part_id=None):
    part_details = None

    if part_id is None:
        clear_screen()
        print("\nBy the Part ID what part would you like the details for? ")
        print("'m' for Main Menu")
        user_input = input("Option: ").lower()

        clear_screen()
        if user_input == 'm':
            return None

        for item in inventory_data.items:
            if item.id.lower() == user_input.lower():
                part_details = item

        part_name = part_details.name
        part_price = part_details.price
        part_id = part_details.id
        part_type = part_details.type
        part_power = None
        other_attr = []

        for attr, value in vars(part_details).items():
            if attr == 'type':
                if value != "PSU":
                    part_power = part_details.power_draw
                else:
                    part_power = part_details.power_supplied

            if attr not in ('name', 'price', 'id', 'type', 'power_draw', 'power_supply'):
                other_attr.append({attr: value})

        print(f"{part_name} ({part_id.lower()})")
        print(f"\tType: {part_type}")
        print(f"\tPrice: ${part_price:,}.00")
        print(f"\tPower: {part_power}W")

        for other_attr_data in other_attr:
            for attr, value in other_attr_data.items():
                print(f"\t{attr}: {value}")

    else:
        # If part_id is provided, directly find the part.
        for item in inventory_data.items:
            if item.id.lower() == part_id.lower():
                return item
