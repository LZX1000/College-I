import os

def yes_or_no():
        response = input().strip().lower()

        if response in ["y", "yes", "1"]:
            return "y"
        elif response in ["n", "no", "0"]:
            return "n"
        else:
            print('\nPlease enter "Y" or "N".\n')
            return yes_or_no()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_value_error():
    try:
        return int(input())
    except ValueError:
        print("\nPlease enter a valid integer.\n")
        return handle_value_error()

def main():
    print("I am but a humble module file.")

if __name__ == "__main__":
    main()