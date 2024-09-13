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
            