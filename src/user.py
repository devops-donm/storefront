class User:
    def __init__(self):
        self.user_name = None
        self.budget = 0

    def get_name(self):
        return self.user_name
    
    def get_budget(self):
        return self.budget

    def update_name(self):
        self.user_name = input("What is your name? ")

    def update_budget(self):
        try:
            budget = int(input("What is your budget? "))
            if budget <= 0:
                raise ValueError("Budget must be a positive amount.")
            else:
                self.budget = budget
        except ValueError as e:
            print(f"Invalid input. {e} Please enter a valid positive integer.")