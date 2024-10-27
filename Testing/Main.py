from Nim import main as nim
from Word_Guess import main as word_guess
from Number_Guess import main as number_guess
from Extras import handle_value_error, clear_screen

def menu_choice(menu_dict):
    choice = handle_value_error()

    if choice in menu_dict.values():
        return list(menu_dict.keys())[list(menu_dict.values()).index(choice)]
    else:
        print("Invalid choice.")
        return menu_choice(menu_dict)

def main():
    menu = ["Quit", "Nim", "Word Guess", "Number Guess"]

    menu_dict = {index: item for index, item in enumerate(menu)}

    clear_screen()

    print("Which game would you like to play?\n")
    print(("\n".join(f"{index}: {item}" for index, item in enumerate(menu))))

    choice_name = list(menu_choice(menu_dict).strip().lower())

    choice_name = "_".join([char for char in choice_name if char != " "])

    eval(choice_name)()


if __name__ == "__main__":
    main()