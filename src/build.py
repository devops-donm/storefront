from src.utils import clear_screen

class Build:
    def __init__(self, user_object, cart_object, inventory_object):
        self.user_object = user_object
        self.cart_object = cart_object
        self.inventory_object = inventory_object

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
        print("Not a valid option, please try again.")

    def update_cost(self, amount):
        self.total_cost = self.total_cost + int(amount)

    def update_power_draw(self, item_type, wattage):
        if item_type != "PSU":
            wattage = wattage * -1
        
        self.total_power_draw = self.total_power_draw + wattage

    def add_item(self, part_id=None):
        clear_screen()
        if part_id is None:
            print("What is the part ID of the item you want to add?")
            part_id = input("Item ID: ")
            clear_screen()
        
            for item in self.inventory_object.items:
                if item.id.lower() == part_id.lower():
                    if item.type.lower() == "ram" or item.type.lower() == "storage":
                        self.build[item.type].append(item)
                    else:
                        self.build[item.type] = item
                    
                    self.update_cost(item.price)
                    
                    if item.type != "PSU":
                        self.update_power_draw(item.type, item.power_draw)
                    else:
                        self.update_power_draw(item.type, item.power_supplied)
        else:
            #TODO: If part_id is provided, directly find the part.
            pass

    def remove_item(self):
        clear_screen()
        print("What is the part type or part ID of the item you want to remove?")
        part = input("Item: ")

        for item in self.inventory_object.items:
            if item.id.lower() == part.lower() or item.type.lower() == part.lower():
                if item.type.lower() == "ram" or item.type.lower() == "storage":
                    if len(self.build[item.type]) <= 1:
                        self.build[item.type] = []
                    else:
                        print(f"What is the {item.type} ID?")
                        user_input = input(f"{item.type} ID: ")
                    
                        for value in self.build[item.type]:
                            if value.id.lower() == user_input.lower():
                                self.build[item.type].remove(value)
                                break
                else:
                    self.build[item.type] = None

    def clear_build(self):
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
        else:
            clear_screen()
            self.default()

    def add_to_cart(self):
        self.cart_object.add_build(self.build)

    def display_build_list(self):
        #TODO: This will need to be cleaned up later.
        for item, data in self.build.items():
            if not data:
                print(f"{item}: None")
            else:
                #TODO: Need to make this look better. UX/UI only shows object data
                # do to RAM and Storage lists.
                print(f"{item}: {data}")

    def build_display(self):
        print("--------------------------------------------------------------------------")
        print(f"Name:   {self.user_object.get_name()}")
        print(f"Budget: ${self.user_object.get_budget()}.00")
        print("--------------------------------------------------------------------------")
        print(f"Total Cost: ${self.total_cost}")
        print(f"Power Draw: {self.total_power_draw}W")
        print("--------------------------------------------------------------------------")
        print("1. add item")
        print("2. remove item")
        print("3. clear build")
        print("4. add build to cart")
        print("5. main menu")
        print("--------------------------------------------------------------------------")

    def build_menu(self):
        clear_screen()
        while True:
            self.display_build_list()
            
            self.build_display()
            user_input = input("\nSelect an option: ").strip().lower()

            # Break the while loop and return to the main menu
            if user_input == "5" or user_input == 'm' or user_input == 'main_menu':
                clear_screen()
                break

            menu_dict: dict = {
                "1": self.add_item,
                "2": self.remove_item,
                "3": self.clear_build,
                "4": self.add_to_cart
            }
            run_option = menu_dict.get(user_input, self.default)
            run_option()