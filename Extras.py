import os, keyboard, time

def yes_or_no(prompt=""):
    while True:
        response = input(prompt).strip().lower()
        if response in ["y", "yes", "1"]:
            return "y"
        elif response in ["n", "no", "0"]:
            return "n"
        else:
            clear_screen('Please enter "Y" or "N".\n')

def clear_screen(prompt=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    if prompt != "":
        print(prompt)

def handle_value_error(prompt=""):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            clear_screen("Please enter a valid integer.\n")

def check_menu_choice(menu, prompt=''):
    while True:
        choice = input(prompt)
        try:
            if int(choice) in range(len(menu)):
                return menu[int(choice)]
        except ValueError:
            if choice.strip().lower().replace(" ", "_") in [item.strip().lower().replace(" ", "_") for item in menu]:
                return choice
        clear_screen("Invalid choice.\n")

def main():
    print("I am but a humble module file.")

if __name__ == "__main__":
    main()