import sys
from src.utils import clear_screen

class Cart:
    def __init__(self, user_object, inventory_object):
        self.user_object = user_object
        self.inventory_object = inventory_object
        
        self.total_cost: int = 0
        self.build_cost: int = 0
        self.cart = {}
    
    def default(self):
        clear_screen()
        print("Not a valid option, please try again.")
    
    def checkout(self):
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
        self.build_cost = 0
        self.cart["BUILD"] = build_data
        self.build_cost += build_cost
        self.total_cost += self.build_cost

    def remove_item(self, part_id=None):
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
            del self.cart[part_id.upper()]
            clear_screen()
            print(f"{item_name} was successfully removed from your cart.\n")
    
    def clear_cart(self):
        clear_screen()
        print("Are you sure you wish to clear the cart. You will lose all data.")
        user_input = input("Yes/No: ")
        if user_input.lower() == 'yes' or user_input.lower() == 'y':
            self.cart = {}
            clear_screen()
        else:
            clear_screen()
            pass
    
    def cart_display(self):
        if not self.cart:
            print("Your cart is currently empty.")
        else:
            for item_key, item_object in self.cart.items():
                if item_key == "BUILD":
                    print("Custom PC Build")
                    print(f"    Motherboard:\n         {item_object["Motherboard"].name} ({item_object["Motherboard"].id.lower()}) - ${item_object["Motherboard"].price:,}.00")
                    print(f"    CPU:\n         {item_object["CPU"].name} ({item_object["CPU"].id.lower()}) - ${item_object["CPU"].price:,}.00")
                    
                    if item_object["GPU"]:
                        print(f"    GPU:\n         {item_object["GPU"].name} ({item_object["GPU"].id.lower()}) - ${item_object["GPU"].price:,}.00")
                    print(f"    PSU:\n         {item_object["PSU"].name} ({item_object["PSU"].id.lower()}) - ${item_object["PSU"].price:,}.00")
                    
                    if item_object["RAM"]:
                        if len(item_object["RAM"]) == 1:
                            print(f"    RAM:\n         {item_object["RAM"][0].name} ({item_object["RAM"][0].id.lower()}) - ${item_object["RAM"][0].price:,}.00")
                        else:
                            print("    RAM:")
                            for dimm in item_object["RAM"]:
                                print(f"         {dimm.name} ({dimm.id.lower()}) - ${dimm.price:,}.00")
                    
                    if item_object["Storage"]:
                        if len(item_object["Storage"]) == 1:
                            print(f"    Storage:\n         {item_object["Storage"][0].name} ({item_object["Storage"][0].id.lower()}) - ${item_object["Storage"][0].price:,}.00")
                        else:
                            print("    Storage:")
                            for drive in item_object["Storage"]:
                                print(f"         {drive.name} ({drive.id.lower()}) - ${drive.price:,}.00")
                    print("")
                else:
                    print(f"{item_object.name} ({item_object.id.lower()}) - ${item_object.price:,}.00")
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
        clear_screen()
        while True:
            self.cart_display()
            user_input = input("\nSelect an option: ").strip().lower()

            # Break the while loop and return to the main menu
            if user_input == "m" or user_input == 'M' or user_input == 'main_menu':
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