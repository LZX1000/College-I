import random, keyboard
from Extras import yes_or_no, clear_screen, handle_value_error, check_menu_choice

def main(active_user='Guest', highscore=None):
    main_menu = ["Quit", "Play Game", "Settings"]
    settings_menu = ["Change high bound", "Change low bound", "Back to game"]
    high_bound = 100
    low_bound = 1
    
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
                    new_high_bound = handle_value_error("Enter a new high bound: ")
                    if new_high_bound > low_bound:
                        high_bound = new_high_bound
                elif settings_choice == 'Change low bound':
                    clear_screen()
                    new_low_bound = handle_value_error("Enter a new low bound: ")
                    if new_low_bound < high_bound:
                        low_bound = new_low_bound
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
                if highscore == None or guesses < highscore:
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