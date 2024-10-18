"""
This module provides a User class for managing user information including name and budget.
It includes methods for updating and retrieving these attributes.

Acknowledged Pylint Standard Errors:
src\\user.py:5:0: E0401: Unable to import 'src.utils' (import-error)
"""
from src.utils import clear_screen # pylint: disable=import-error

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
            if  len(name) >= max_length:
                clear_screen()
                print(f"The name you entered exceeds the max length ({max_length}).")
                print("Please try again.")
            else:
                self.user_name = name
                clear_screen()
                break

    def update_budget(self):
        """
        Prompts the user to input a valid positive integer for the budget
        and updates the budget attribute. If the input is invalid or 0, prompts again.
        """
        clear_screen()

        while True:
            try:
                budget = int(input("What is your budget? "))
                if budget == 0:
                    print("Your budget can't be 0. Please try again.")
                elif budget < 0:
                    print("Budget must be a positive integer. Please try again.")
                else:
                    self.budget = budget
                    print(f"Budget updated to {self.budget}.")
                    break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
