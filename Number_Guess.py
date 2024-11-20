import random, keyboard
from Extras import yes_or_no, clear_screen, handle_value_error, check_menu_choice

def main(active_user='Guest'):
    main_menu = ["Quit", "Play Game", "Settings"]
    settings_menu = ["Change high bound", "Change low bound", "Back to game"]
    clear_screen()
    menu_choice = check_menu_choice(main_menu, "\n".join([f"{index} : {main_menu[index]}" for index in range(len(main_menu))]) + "\n\n")

    if menu_choice == 'Quit':
        return 'Number Guess', active_user
    elif menu_choice == 'Settings':
        settings_choice = check_menu_choice(settings_menu, "\n".join([f"{index} : {settings_menu[index]}" for index in range(len(settings_menu))]) + "\n\n")

if __name__ == "__main__":
    main()