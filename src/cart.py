from src.utils import clear_screen

class Cart:
    def __init__(self, user_object, inventory_object):
        self.user_object = user_object
        self.inventory_object = inventory_object
        
        self.total_cost: int = 0
        self.total_power: int = 0
        self.cart = {}
    
    def default(self):
        print("Not a valid option, please try again.")
    
    def add_item(self, part_id=None):
        clear_screen()
        if part_id is None:
            print("What is the item ID of the part you want to add?")
            part_id = input("Item ID: ")
            
        part_data = self.inventory_object.get_details(part_id)

        if part_data is None:
            '''
            if part_data is still None after user_input then part_id is not in inventory.
            '''
            clear_screen()
            self.default()
        
        clean_part_data = part_data["item"]

        if not self.cart:
            self.cart[clean_part_data["id"]] = {
                "name": clean_part_data["name"],
                "type": clean_part_data["type"],
                "price": clean_part_data["price"],
                "quantity": 1,
                "power_draw": clean_part_data["power_draw"],
                "part_data": clean_part_data
            }
            self.total_cost = self.total_cost + int(clean_part_data["price"])
            self.total_power = self.total_power + int(clean_part_data["power_draw"])

        elif clean_part_data['id'] in self.cart:
            self.cart[part_id.upper()]["quantity"] += 1
            self.total_cost = self.total_cost + int(clean_part_data["price"])
            self.total_power = self.total_power + int(clean_part_data["power_draw"])
        else:
            clear_screen()
            self.default()

        clear_screen()
        print("Your cart has been updated.\n")
    
    def remove_item(self, part_id=None):
        clear_screen()
        if part_id is None:
            print("What is the item ID of the part you want to remove?")
            part_id = input("Item ID: ")
        
        if part_id.upper() in self.cart:
            del self.cart[part_id.upper()]
            clear_screen()
            print(f"{part_id} was successfully removed from your cart.")
    
    def clear_cart(self):
        clear_screen()
        print("Are you sure you wish to clear the cart. You will lose all data.")
        user_input = input("Yes/No: ")
        if user_input.lower() == 'yes' or user_input.lower() == 'y':
            self.cart = {}
            clear_screen()
        else:
            clear_screen()
    
    def cart_display(self):
        print("--------------------------------------------------------------------------")
        print(f"Name:   {self.user_object.get_name()}")
        print(f"Budget: ${self.user_object.get_budget()}.00")
        print("--------------------------------------------------------------------------")
        print(f"Total Cost: ${self.total_cost}")
        print("--------------------------------------------------------------------------")
        print("1. add_item")
        print("2. remove_item")
        print("3. clear_cart")
        print("4. main_menu")
        print("--------------------------------------------------------------------------")

    def cart_menu(self):
        clear_screen()
        while True:
            if not self.cart:
                print("Your cart is currently empty.\n")
            else:
                for item_id, item_info in self.cart.items():
                    print(item_info["name"])
            
            self.cart_display()
            user_input = input("\nSelect an option: ").strip().lower()

            # Break the while loop and return to the main menu
            if user_input == "4" or user_input == 'm' or user_input == 'main_menu':
                clear_screen()
                break

            menu_dict: dict = {
                "1": self.add_item,
                "2": self.remove_item,
                "3": self.clear_cart
            }
            run_option = menu_dict.get(user_input, self.default)
            run_option()