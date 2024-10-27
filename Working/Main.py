from Nim import main as nim
from Word_Guess import main as word_guess
from Extras import handle_value_error, clear_screen

def menu_choice(menu):
    choice = handle_value_error()

    if choice in range(len(menu)):
        return menu[choice]

    else:
        print("Invalid choice.")
        return menu_choice(menu)

def run_choice():
    print()

def main():
    menu = ["Quit", "Nim", "Word Guess"]

    clear_screen()

    print("Which game would you like to play?\n")
    print("\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]))

    choice_name = (menu_choice(menu).strip().lower()).replace(" ", "_")

    eval((choice_name + '()'))

if __name__ == "__main__":
    main()