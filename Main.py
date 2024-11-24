from Nim import main as nim
from Word_Guess import main as word_guess
from The_Arena import main as the_arena
from Snake import main as snake
from Number_Guess import main as number_guess
from Extras import clear_screen, yes_or_no, check_menu_choice
from Start import main as start_main

def sign_in():
    """
    Handles user sign-in and account creation.

    This function prompts the user to either sign in with an existing account or create a new one.
    It reads from or writes to a file named "stats.txt" to store user credentials.

    Returns:
        tuple: A tuple containing the username and password of the signed-in or newly created account.
        bool: A boolean indicating successful sign-in or account creation.
    """
    clear_screen()
    response_1 = ""
    while True:
        #Open existing users file or create a new one
        try:
            with open("stats.txt", "r") as file:
                file_lines = file.readlines()
                for line in file_lines:
                    if line and line[0] == " ":
                        continue
                    else:
                        users = [tuple(line.strip().split(', ')) for line in file.readlines()]
        except FileNotFoundError:
            with open("stats.txt", "w") as file:
                users = []
        if response_1 != "y":
            response = yes_or_no("Do you already have an account? (Y/N)\n\n")
        #Sign in
        if response == "y" or response_1 == "y":
            clear_screen()
            username_try = input("Username: ").strip()
            password_try = input("\nPassword: ")
            attempt = (username_try, password_try)
            if attempt in users:
                #Correct credentials
                clear_screen(f"Welcome, {username_try}!")
                return attempt, True
            else:
                clear_screen("Invalid username or password.")
        #Create new account
        elif response == "n":
            clear_screen("What should we call you?\n")
            new_user = input("Username: ").strip()
            while True:
                #Check if username is valid
                if not new_user:
                    clear_screen("Please enter a valid username.")
                    new_user = input("Username: ").strip()
                else:
                    for char in new_user:
                        if char == " " or char == ",":
                            clear_screen("Please enter a valid username.")
                            new_user = input("Username: ").strip()
                    if any(new_user == user[0] for user in users) or new_user == "Guest":
                        clear_screen("That username is already taken.\nWould you like to sign in? (Y/N)\n")
                        response_1 = yes_or_no()
                        if response_1 == "y":
                            clear_screen()
                            break
                        elif response_1 == "n":
                            clear_screen()
                            new_user = input("Username: ").strip()
                    #Not taken, make a password
                    else:
                        new_pass = input("\nPassword: ")
                        attempt = (new_user, new_pass)
                        users.append(attempt)
                        with open("stats.txt", "a") as file:
                            file.write(f"{new_user}, {new_pass}\n")
                        return attempt, True

def update_game_stats(game, active_account, highscore=[]):
    """
    Updates the game statistics for a given user in the stats.txt file.

    Parameters:
    game (str): The name of the game to update stats for.
    active_account (tuple): A tuple containing the user's account information (username, user_id).
    highscore (list or int, optional): A list of high scores or a single high score to update. Defaults to an empty list.

    Raises:
    FileNotFoundError: If the "stats.txt" file does not exist and cannot be created.
    Exception: If an error occurs while attempting to create the stats file.
    """
    # Convert highscore to a list if it is an integer
    if isinstance(highscore, int):
        highscore = [highscore]
    if highscore is None:
        highscore = ["None"]
    # Open file if it exists
    try:
        main_line = None
        sublines = []
        with open("stats.txt", "r+") as file:
            # Read file and initialize user_found variable
            file_lines = file.readlines()
            user_found = False
            # Find user
            for i, line in enumerate(file_lines):
                if f"{active_account[0]}, {active_account[1]}" in line:
                    user_found = True
                    main_line = line
                    main_line_number = i
                    break
            # If user not found, add user to file
            if not user_found:
                file_lines.append(f"{active_account[0]}, {active_account[1]}\n")
                main_line = file_lines[-1]
                main_line_number = len(file_lines) - 1
            # Identify sublines
            for subline in file_lines[main_line_number + 1:]:
                if len(subline) - len(subline.lstrip()) > len(main_line) - len(main_line.lstrip()):
                    sublines.append(subline)
                else:
                    break
            # Update game stats
            for i, subline in enumerate(sublines):
                if game in subline:
                    stats = subline.strip().split(", ")
                    stats[1] = str(int(stats[1]) + 1)
                    stats_highscores = list(map(int, stats[2].split(" ")))
                    for i, stats_highscore in enumerate(stats_highscores):
                        if highscore[i] is not None and highscore[i] != "None" and highscore[i] > stats_highscore:
                            stats_highscores[i] = highscore[i]
                        else:
                            stats_highscores[i] = stats_highscore if stats_highscore != "None" else highscore[i]
                    sublines[i] = f"    {game}, {stats[1]}, {' '.join(map(lambda x: str(x) if x is not None else 'None', stats_highscores))}\n"
                    break
            # If game not found, add game to user
            else:
                sublines.append(f"    {game}, 1, {' '.join(map(lambda x: str(x) if x is not None else 'None', highscore))}\n")
            # Write updated stats to file
            file.seek(0)
            file.writelines(file_lines[:main_line_number + 1] + sublines + file_lines[main_line_number + 1 + len(sublines):])
    # If file does not exist, create file and write user and game stats
    except FileNotFoundError:
        try:
            with open("stats.txt", "w") as file:
                file.write(f"{active_account[0]}, {active_account[1]}\n" + f"    {game}, 1, {' '.join(map(lambda x: str(x) if x is not None else 'None', highscore))}\n")
        # If an error occurs while attempting to create the stats file, raise and print an exception
        except Exception as e:
            print(f"An error occured while attempting to create the stats file: {e}")

def main():
    """
    Main function that handles the user sign-in process and game menu navigation.

    The function runs an infinite loop that:
    1. Prompts the user to sign in.
    2. Displays a menu of games to the signed-in user.
    3. Executes the selected game or handles sign-out/quit actions.

    The function updates game statistics after each game is played.

    Does not return
    """
    while True:
        active_account, signed_in = sign_in()
        while signed_in == True:
            #Defines the games in the menu as a list
            menu = ["Quit", "Sign Out", "Nim", "Number Guess", "Word Guess", "The Arena", "Snake"]
            clear_screen()
            #Gets a proper input
            choice = check_menu_choice(menu, "Which game would you like to play?\n\n" + "\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]) + "\n\n").strip().lower().replace(" ", "_")
            #Executes the choice
            if choice == "quit":
                return
            elif choice == "sign_out":
                signed_in = False
            else:
                game, active_account, highscore, = eval(choice)(active_account)
                update_game_stats(game, active_account, highscore)

if __name__ == "__main__":
    main()