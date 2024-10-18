"""
Utility function to clear the terminal screen.

Uses 'cls' for Windows and 'clear' for other operating systems.

This function is part of the utils.py module.
"""
import os

def clear_screen():
    """
    Clears the terminal screen using 'cls' for Windows and 'clear' for other systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
