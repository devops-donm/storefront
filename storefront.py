import sys

def get_budget():
    """
    Prompt the user to enter their budget.

    Returns:
        int: The user's budget.
    """
    while True:
        try:
            budget = int(input("What is your budget? "))
            if budget <= 0:
                raise ValueError("Budget must be a positive amount.")
            else:
                return budget
        except ValueError as e:
            print(f"Invalid input. {e} Please enter a valid positive integer.")

def main():
    user_name = input("What is your name? ")
    budget = get_budget()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye")