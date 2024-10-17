from src.utils import clear_screen

class Build:
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
        print("Not a valid option, please try again.")

    def increase_total_cost(self, amount):
        self.total_cost += amount
    
    def decrease_total_cost(self, amount):
        self.total_cost -= amount

    def increase_available_power(self, wattage):
        self.total_power_draw += wattage

    def decreate_available_power(self, wattage):
        self.total_power_draw -= wattage

    def add_item(self, part_id=None):
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
        else:
            #TODO: If part_id is provided, directly find the part.
            pass

    def remove_item(self):
        clear_screen()
        print("What is the part type of the item you want to remove?")
        part = input("Part Type: ")

        for item in self.inventory_object.items:
            if item.type.lower() == part.lower():
                if item.type.lower() == "ram" or item.type.lower() == "storage":
                    if len(self.build[item.type]) == 0:
                        self.build[item.type] = []
                        clear_screen()
                        print(f"Nothing in {item.type} to delete.")
                    elif len(self.build[item.type]) == 1:
                        self.build[item.type] = []
                        #TODO: adjust cost / power draw
                        clear_screen()
                        print(f"Item has been removed from {item.type}.")
                    elif len(self.build[item.type]) > 1:
                        clear_screen()
                        user_input = input(f"What is the {item.type} Part ID: ")
                        for ram_object in self.build[item.type]:
                            if ram_object.id.lower() == user_input.lower():
                                self.build[item.type].remove(ram_object)
                                #TODO: adjust cost / power draw
                                break
                else:
                    self.build[item.type] = None
                    clear_screen()
                    print(f"{item.name} ({item.id}) was removed from build.\n")

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
        compatibility_test = self.compatibility_object.build_check(self.build, self.total_power_draw)
        if compatibility_test:
            self.cart_object.add_build(self.build, self.total_cost)
            clear_screen()
            print("Build has been added to the shopping cart!")
        else:
            clear_screen()
            print("Build is not compatible. See Build - Compatibility Check for more information.")

    def display_build_list(self):
        #TODO: This will need to be cleaned up later.
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
                    print(f"    {item_object.name} ({item_object.id.lower()}) - ${item_object.price:,}.00")


    def build_display(self):
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
        clear_screen()
        while True:
            self.display_build_list()
            
            self.build_display()
            user_input = input("\nSelect an option: ").strip().lower()

            # Break the while loop and return to the main menu
            if user_input == "m" or user_input == 'M' or user_input == 'main_menu':
                clear_screen()
                break

            menu_dict: dict = {
                "1": self.add_item,
                "2": self.remove_item,
                "3": lambda: self.compatibility_object.build_check(self.build, self.total_power_draw),
                "4": self.clear_build,
                "5": self.add_to_cart
            }
            run_option = menu_dict.get(user_input, self.default)
            run_option()