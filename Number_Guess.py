import random, keyboard
from Extras import Player, yes_or_no, clear_screen, handle_int_input, check_menu_choice

def main(active_user=Player("Guest", "")):
    """
    Main function to run the Number Guess game.
    The function provides a main menu with options to Quit, Play Game, or access Settings.
    In the Settings menu, users can change the low and high bounds for the guessing range.
    The Play Game option starts the number guessing game where the user tries to guess a randomly generated number within the specified bounds.
    The game tracks the number of guesses and updates the highscore if a new best score is achieved

    Parameters:
    active_user (str): The username of the active user. Default is 'Guest'.

    Returns:
    tuple: A tuple containing the game name 'Number Guess' and the active user's name..
    """
    main_menu = ["Quit", "Play Game", "Settings"]
    settings_menu = ["Back to game", "Change low bound", "Change high bound"]
    high_bound = 100
    low_bound = 1
    highscore = None
    
    while True:
        clear_screen()
        menu_choice = check_menu_choice(main_menu, "\n".join([f"{index} : {main_menu[index]}" for index in range(len(main_menu))]) + "\n\n")

        if menu_choice == 'Quit':
            return 'Number Guess', active_user, None
        elif menu_choice == 'Settings':
            while True:
                clear_screen()
                settings_choice = check_menu_choice(settings_menu, "\n".join([f"{index} : {settings_menu[index]}" for index in range(len(settings_menu))]) + "\n\n")

                if settings_choice == 'Change high bound':
                    clear_screen()
                    while True:
                        new_high_bound = handle_int_input("Enter a new high bound: ")
                        if new_high_bound > low_bound:
                            high_bound = new_high_bound
                            break
                        else:
                            clear_screen("High bound must be greater than low bound.\n")
                elif settings_choice == 'Change low bound':
                    clear_screen()
                    while True:
                        new_low_bound = handle_int_input("Enter a new low bound: ")
                        if new_low_bound < high_bound and new_low_bound >= 0:
                            low_bound = new_low_bound
                            break
                        else:
                            clear_screen("Low bound must be less than high bound.\n")
                elif settings_choice == 'Back to game':
                    break
        
        elif menu_choice == 'Play Game':
            Playing = True
            while Playing == True:
                secret_number = random.randint(low_bound, high_bound)
                lowest_guess = low_bound
                highest_guess = high_bound
                guesses = 0
                clear_screen()

                while True:
                    if lowest_guess == highest_guess:
                        clear_screen(f"Unfortunately you were unable to guess the number.\n")
                        break

                    playing_screen = [f"Between : {lowest_guess} - {highest_guess}", f"Guesses : {guesses}", "", "Guess: "]
                    guess = handle_int_input("\n".join(playing_screen))

                    if guess == secret_number:
                        guesses += 1
                        clear_screen(f"Congratulations! You guessed the number in {guesses} guesses.\n")
                        break
                    elif guess > high_bound or guess < low_bound:
                        clear_screen(f"Please enter a valid guess between {low_bound} and {high_bound}.\n")
                    elif guess < secret_number:
                        clear_screen("Too low!\n")
                        guesses += 1
                        if guess >= lowest_guess:
                            lowest_guess = guess + 1
                    elif guess > secret_number:
                        clear_screen("Too high!\n")
                        guesses += 1
                        if guess <= highest_guess:
                            highest_guess = guess - 1
                if highscore == None or guesses < highscore:
                    print("You got a new best score!\n" + f"Best score: {guesses}")
                    highscore = guesses
                response = yes_or_no("Would you like to play again? (Y/N)\n")
                if response == 'n':
                    Playing = False
                    break
                if response == 'y':
                    continue

if __name__ == "__main__":
    main()