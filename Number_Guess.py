import random, keyboard
from Extras import yes_or_no, clear_screen, handle_value_error, check_menu_choice

def main(active_user='Guest', highscore=None):
    main_menu = ["Quit", "Play Game", "Settings"]
    settings_menu = ["Change high bound", "Change low bound", "Back to game"]
    
    while True:
        clear_screen()
        menu_choice = check_menu_choice(main_menu, "\n".join([f"{index} : {main_menu[index]}" for index in range(len(main_menu))]) + "\n\n")

        if menu_choice == 'Quit':
            return 'Number Guess', active_user
        elif menu_choice == 'Settings':
            while True:
                clear_screen()
                settings_choice = check_menu_choice(settings_menu, "\n".join([f"{index} : {settings_menu[index]}" for index in range(len(settings_menu))]) + "\n\n")

                if settings_choice == 'Change high bound':
                    clear_screen()
                    high_bound = handle_value_error("Enter a new high bound: ")
                elif settings_choice == 'Change low bound':
                    clear_screen()
                    low_bound = handle_value_error("Enter a new low bound: ")
                elif settings_choice == 'Back to game':
                    break
        
        elif menu_choice == 'Play Game':
            Playing = True
            while Playing == True:
                try:
                    secret_number = random.randint(low_bound, high_bound)
                    lowest_guess = low_bound
                    highest_guess = high_bound
                except NameError:
                    secret_number = random.randint(1, 100)
                    lowest_guess = 1
                    highest_guess = 100
                guesses = 0
                clear_screen()

                while True:
                    playing_screen = [f"Between : {lowest_guess} - {highest_guess}", f"Guesses : {guesses}", "", "Guess: "]
                    guess = handle_value_error("\n".join(playing_screen))

                    if guess == secret_number:
                        clear_screen(f"Congratulations! You guessed the number in {guesses} guesses.\n")
                        break
                    elif guess < secret_number:
                        clear_screen("Too low!\n")
                        guesses += 1
                        if guess > lowest_guess:
                            lowest_guess = guess + 1
                    elif guess > secret_number:
                        clear_screen("Too high!\n")
                        guesses += 1
                        if guess < highest_guess:
                            highest_guess = guess - 1
                if guesses < highscore or highscore == None:
                    print("You got a new bestscore!\n" + f"Best score: {guesses}")
                    highscore = guesses
                response = yes_or_no("Would you like to play again? (Y/N)\n")
                if response == 'n':
                    Playing = False
                    break
                if response == 'y':
                    continue

if __name__ == "__main__":
    main()