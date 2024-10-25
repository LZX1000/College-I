import random
import keyboard
from Extras import yes_or_no, clear_screen

def menu():
    menu = ["Play", "Highscores", "Settings", "Exit"]

    menu_dict = {item: index for index, item in enumerate(menu)}

    choice = input("\n".join(f"{index}: {item}" for index, item in enumerate(menu))).strip()

    if choice in menu_dict:
        choice_index = menu_dict[choice].lower()
        {choice_index}()
    else:
        print("Invalid choice.")

def check_highscore():

    highscores = []

    if len(highscores) < 5:
        highscores.append((USERNAME, GUESSES))

    return highscores

def highscores():
    print("\n".join(f"{name}: {score}" for name, score in H_LIST.items()))

    print("Press any key to continue...")
    keyboard.read_key()

def settings():
    settings = ["Back", "Bounds", "Highscore"]

    settings_dict = {item: index for index, item in enumerate(settings)}

    choice = input(f"What would you like to see?\n" "\n".join(f"{index}: {item}" for index, item in enumerate(menu))).strip()

    if choice in settings.dict:
        choice_index = settings_dict[choice].lower()
        {choice_index}()

def back():
    menu()

def bounds():
    MAXIMUM = input("Enter a new high bound: ")
    MINIMUM = input("Enter a new low bound: ")
    
    settings()

def highscore():
    print("Are you sure you want to reset your current highscores?")

    choice = yes_or_no()

    if choice == "y":
        reset_highscores()
        settings()

    elif choice == "n":
        settings()

def try_again():
    '''
        print(f"{CURRENT_PLAYER} lost. Try again? (Y/N)\n")
    '''
    while True:
        response = input().lower()

        if response == "y":
            clear_screen()
            play()
        elif response == "n":
            exit()
        else:
            print('\nPlease enter "Y" or "N".\n')

def get_random_number():
    return random.randint()

def guessing():
    guess = input()

    GUESSES += 1

    if guess == GAME_NUMBER:
        print(f"\nCongrats! You guessed it in {GUESSES} guesses.")

    elif guess > GAME_NUMBER:
        print("\nLower\n")
        guessing()

    elif guess < GAME_NUMBER:
        print("\nHigher\n")
        guessing()

    else:
        print(f"\nPlease enter a valid intiger between {MINIMUM} and {MAXIMUM}.\n")
        guessing()

def play(username):
    global GUESSES
    global GAME_NUMBER
    global MAXIMUM
    global MINIMUM
    global USERNAME
    global H_LIST

    USERNAME = username
    GAME_NUMBER = get_random_number()
    GUESSES = 0

    print(f"Choose a number between {MINIMUM} and {MAXIMUM}.\n")
    guessing()

if __name__ == '__main__':
    play()