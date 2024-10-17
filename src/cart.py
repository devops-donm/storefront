from src.utils import clear_screen

class Cart:
    def __init__(self, user_object, inventory_object):
        self.user_object = user_object
        self.inventory_object = inventory_object
        
        self.total_cost: int = 0
        self.build_cost: int = 0
        self.cart = {}
    
    def default(self):
        print("Not a valid option, please try again.")
    
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
                self.total_cost = self.total_cost - int(self.cart[part_id.upper()].price)
            del self.cart[part_id.upper()]
            clear_screen()
            print(f"{part_id} was successfully removed from your cart. {part_id}")
    
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
        print("--------------------------------------------------------------------------")
        print(f"Name:   {self.user_object.get_name()}")
        print(f"Budget: ${self.user_object.get_budget():,}.00")
        print("--------------------------------------------------------------------------")
        print(f"Total Cost: ${self.total_cost:,}.00")
        print("--------------------------------------------------------------------------")
        print("1. add item")
        print("2. remove item")
        print("3. clear cart")
        print("--------------------------------------------------------------------------")
        print("m. main menu")

    def cart_menu(self):
        clear_screen()
        while True:
            if not self.cart:
                print("Your cart is currently empty.\n")
            else:
                print(self.cart)
            
            self.cart_display()
            user_input = input("\nSelect an option: ").strip().lower()

            # Break the while loop and return to the main menu
            if user_input == "m" or user_input == 'M' or user_input == 'main_menu':
                clear_screen()
                break

            menu_dict: dict = {
                "1": self.add_item,
                "2": self.remove_item,
                "3": self.clear_cart
            }
            run_option = menu_dict.get(user_input, self.default)
            run_option()