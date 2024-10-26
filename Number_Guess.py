#Inports

import random
import keyboard
from Extras import yes_or_no, clear_screen, handle_value_error

#Main Menu

def display_menu():
    menu = ["Play", "Highscores", "Settings", "Exit"]

    menu_dict = {item: index for index, item in enumerate(menu)}

    choice = input("\n".join(f"{index}: {item}" for index, item in enumerate(menu))).strip()

    if choice in menu_dict and choice != "Play":
        choice_index = menu_dict[choice].lower()
        {choice_index}()
    elif choice == "play":
        clear_screen()
        main()
    else:
        print("Invalid choice.")

#Checks if there is an available highscore slot in the list of 5, returning highscores either way.

def check_highscore(highscores, guesses):

    if len(highscores) < 5:
        highscores.append((USERNAME, guesses))

    return highscores

#Displays the highscores

def highscores():
    print("\n".join(f"{name}: {score}" for name, score in H_LIST.items()))

    print("Press any key to continue...")
    keyboard.read_key()

#Game Settings Menu

def settings():
    settings = ["Back", "Bounds", "Highscore"]

    settings_dict = {item: index for index, item in enumerate(settings)}

    choice = input(f"What would you like to see?\n" "\n".join(f"{index}: {item}" for index, item in enumerate(settings))).strip()

    if choice in settings.dict:
        choice_index = settings_dict[choice].lower()
        {choice_index}()

#Child function for the settings menu
#Takes you back to the main menu

def back():
    display_menu()

#Child function for the settings menu
#Allows the user to change the bounds of the game

def bounds():
    MAXIMUM = input("Enter a new high bound: ")
    MINIMUM = input("Enter a new low bound: ")
    
    settings()

#Child function for the settings menu
#Resets the highscores

def highscore():
    print("Are you sure you want to reset your current highscores?")

    choice = yes_or_no()

    if choice == "y":
        reset_highscores()
        settings()

    elif choice == "n":
        settings()

def get_highscore(highscores):
    highscores.sort(key=lambda x: x[1], reverse=True)

    return highscores[0][1]

#Try agin? function for when the game ends

def game_over(guesses, highscores):
    print(f"\nCongrats! You guessed it in {guesses} guesses.\n\nThe current highscore is: {get_highscore(highscores)}.\n")

    response = yes_or_no()

    if response == "y":
        clear_screen()
        main()
    elif response == "n":
        exit()

#Checks if the guessed number is within the bounds
def check_number(check, maximum, minimum):
    if check >= minimum and check <= maximum:
        return check
    else:
        print(f"\nPlease enter a valid integer between {minimum} and {maximum}.\n")
        check = handle_value_error()
        check_number(check)

#Guessing Loop

def guessing(game_number, guesses, highscores, maximum, minimum):
    guess = check_number(maximum, minimum, check=handle_value_error())

    guesses += 1

    if guess == game_number:
        game_over(guesses, highscores)

    elif guess > game_number:
        print("\nLower\n")
        guessing()

    elif guess < game_number:
        print("\nHigher\n")
        guessing()

    else:
        print(f"\nPlease enter a valid integer between {minimum} and {maximum}.\n")
        guessing()

def main():
    game_number = random.randint()
    guesses = 0
    highscores = []
    maximum = 100
    minimum = 1

    global USERNAME
    global H_LIST

    USERNAME = username

    print(f"Choose a number between {MINIMUM} and {MAXIMUM}.\n")
    guessing(game_number, guesses, highscores, maximum, minimum)

if __name__ == '__main__':
    main()