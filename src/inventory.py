from src.utils import clear_screen

class Inventory:
    def __init__(self, inventory_data):
        self.inventory_data = inventory_data

        self.available_category_options = [
                                            "all",
                                            "cpu",
                                            "gpu",
                                            "ram",
                                            "psu",
                                            "motherboard",
                                            "storage"
                                        ]
    def print_categories(self):
        for category in self.available_category_options:
            print(category)

    def list_parts(self):
        """
        Fuction to list parts from inventory based on user-specified category.
        """
        self.print_categories()
        print("\nFrom the provided categories what would you like to list? ")
        user_input = input("Option: ").lower()

        if user_input == 'all':
            clear_screen()
            for item_keys in self.inventory_data["inventory"]:
                item = item_keys["item"]
                print(item)
        else:
            filtered_items = [
                item["item"] for item in self.inventory_data["inventory"]
                if item["item"]["type"].lower() == user_input
            ]

            if not filtered_items:
                clear_screen()
                print(f"No items found in category: {user_input.upper()}")
            else:
                clear_screen()
                for item in filtered_items:
                    print(item)

    def get_details(self, part_id=None):
        part_details = None
        
        if part_id is None:
            print("\nBy the Part ID what part would you like the details for? ")
            print("'m' for Main Menu")
            user_input = input("Option: ").lower()

            if user_input == 'm':
                clear_screen()
                return

            clear_screen()
            for item_keys in self.inventory_data["inventory"]:
                if item_keys["item"]["id"].lower() == user_input:
                    part_details = item_keys
            
            if part_details is None:
                print(f"Part ID {user_input.upper()} did not return a match.")
                print("Please review parts list and try again.\n")
            else:
                print(f"\n{part_details}\n")
        
        else:
            for item_keys in self.inventory_data['inventory']:
                if item_keys['item']['id'].lower() == part_id.lower():
                    part_details = item_keys
            if part_details is None:
                return None
            else:
                return part_details