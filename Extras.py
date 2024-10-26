import os

def yes_or_no():
        response = input().lower()

        if response == "y":
            return response
        elif response == "n":
            return response
        
        else:
            print('\nPlease enter "Y" or "N".\n')
            yes_or_no()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    yes_or_no()

def handle_value_error():
    try:
        return int(input())
    except ValueError:
        print("\nPlease enter a valid integer.\n")
        handle_value_error()

if __name__ == "__main__":
    main()