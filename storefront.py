import sys

def main():
    user_name = input("What is your name? ")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye")