import os, keyboard

class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.username}, {self.password}"

def clear_input():
    keyboard.send('enter')
    input()

def yes_or_no(prompt=""):
    while True:
        print(prompt)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "y" or event.name == "1":
                clear_input()
                return "y"
            elif event.name == "n" or event.name == "0":
                clear_input()
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
        print(prompt)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            try:
                if int(event.name) in range(len(menu)):
                    clear_input()
                    return menu[int(event.name)]
            except ValueError:
                continue
        choice = input()
        if choice.strip().lower().replace(" ", "_") in [item.strip().lower().replace(" ", "_") for item in menu]:
            return choice
        clear_screen("Invalid choice.\n")

def main():
    print("I am but a humble module file.")

if __name__ == "__main__":
    main()