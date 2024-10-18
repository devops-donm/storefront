"""
This module provides a User class for managing user information including name and budget.
It includes methods for updating and retrieving these attributes.
"""
from src.utils import clear_screen

class User:
    """
    Represents a user with a name and budget.
    
    Methods:
    - get_name: Returns the user's name.
    - get_budget: Returns the user's budget.
    - update_name: Prompts the user to input and set their name (with a max length).
    - update_budget: Prompts the user to input and set a valid budget.
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
