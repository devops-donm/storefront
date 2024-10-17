from src.utils import clear_screen

class User:
    def __init__(self):
        self.user_name = None
        self.budget = 0

    def get_name(self):
        return self.user_name
    
    def get_budget(self):
        return self.budget

    def update_name(self, max_length=50):
        clear_screen()
        while True:
            name = input("What is your name? ")
            if  len(name) <= max_length:
                self.user_name = name
                break
            else:
                print(f"The name you entered exceeds the max length ({max_length}).")
                print("Please try again.")

    def update_budget(self):
        clear_screen()
        try:
            budget = int(input("What is your budget? "))
            if budget <= 0:
                raise ValueError("Budget must be a positive amount.")
            else:
                self.budget = budget
        except ValueError as e:
            print(f"Invalid input. {e} Please enter a valid positive integer.")