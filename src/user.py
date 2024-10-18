from src.utils import clear_screen

class User:
    """
    A class to represent a user with a name and budget. 
    Provides methods to update and retrieve these attributes.
    """
    def __init__(self):
        self.user_name = None
        self.budget = 0

    def get_name(self):
        """Returns the user name."""
        return self.user_name
    
    def get_budget(self):
        """Returns the user budget."""
        return self.budget

    def update_name(self, max_length=50):
        """
        Prompts the user to input a name and updates the user_name attribute if the input
        is within the allowed maximum length.
        """
        clear_screen()
        while True:
            name = input("What is your name? ")
            if  len(name) <= max_length:
                self.user_name = name
                clear_screen()
                break
            else:
                clear_screen()
                print(f"The name you entered exceeds the max length ({max_length}).")
                print("Please try again.")

    def update_budget(self):
        """
        Prompts the user to input a valid positive integer for the budget
        and updates the budget attribute. Raises an error if the input is invalid.
        """
        clear_screen()
        try:
            budget = int(input("What is your budget? "))
            if budget <= 0:
                raise ValueError("Budget must be a positive amount.")
            else:
                self.budget = budget
        except ValueError as e:
            print(f"Invalid input. {e} Please enter a valid positive integer.")