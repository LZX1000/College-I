from Nim import main as nim
from Word_Guess import main as word_guess
from The_Arena import main as the_arena
from Snake import main as snake
from Number_Guess import main as number_guess
from Extras import clear_screen, yes_or_no, check_menu_choice
from Start import main as start_main

class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.name}, {self.password}"

def sign_in(users):
    clear_screen()
    response_1 = ""
    while True:
        if response_1 != "y":
            response = yes_or_no("Do you already have an account? (Y/N)\n\n")
        # Sign in
        if response == "y" or response_1 == "y":
            clear_screen()
            username_try = input("Username: ").strip()
            password_try = input("\nPassword: ")
            attempt = (username_try, password_try)
            # Check if the user exists
            for user in users:
                if attempt == (user.username, user.password):
                    #Correct credentials
                    clear_screen(f"Welcome, {username_try}!")
                    return attempt, True
            clear_screen("Invalid username or password.")
        # Create new account
        elif response == "n":
            clear_screen("What should we call you?\n")
            new_username = input("Username: ").strip()
            vaildate_username = lambda username: any(char == " " or char == "," for char in username)
            while True:
                # Check if username is valid
                if vaildate_username(new_username):
                    clear_screen("Please enter a valid username.")
                    new_username = input("Username: ").strip()
                elif any(new_username == user.username for user in users) or new_username == "Guest":
                    clear_screen("That username is already taken.\nWould you like to sign in? (Y/N)\n")
                    response_1 = yes_or_no()
                    if response_1 == "y":
                        clear_screen()
                        break
                    elif response_1 == "n":
                        clear_screen()
                        new_username = input("Username: ").strip()
                # Not taken, make a password
                else:
                    new_user = Player(new_username, input("\nPassword: "))
                    with open("stats.txt", "a") as file:
                        file.write(f"{new_user}\n")
                    return new_user, True

def update_game_stats(game, active_account, highscore=[]):
    # Convert highscore to a list if it is an integer
    if highscore is None:
        highscore = ["None"]
    if isinstance(highscore, int):
        highscore = [highscore]
    # Open file if it exists
    try:
        user_line = None
        sublines = []
        with open("stats.txt", "r+") as file:
            # Read file and initialize user_found variable
            file_lines = file.readlines()
            user_found = False
            # Find user
            for i, line in enumerate(file_lines):
                if f"{active_account[0]}, {active_account[1]}" in line:
                    user_found = True
                    user_line = line
                    user_line_number = i
                    break
            # If user not found, add user to file
            if not user_found:
                file_lines.append(f"{active_account[0]}, {active_account[1]}\n")
                user_line = file_lines[-1]
                user_line_number = len(file_lines) - 1
            # Update game stats
            games_stats = user_line.strip().split("; ")
            for i, game_stats in enumerate(games_stats):
                stats = game_stats.strip().split(", ")   
                if game_stats[0] == game:
                    stats[1] = str(int(stats[1]) + 1)
                    stats_highscores = list(map(lambda x: int(x) if x != "None" else None, stats[2].split(" ")))
                    for j, stats_highscore in enumerate(stats_highscores):
                        if highscore[j] is not None and highscore[j] != "None" and (stats_highscore is None or highscore[j] > stats_highscore):
                            stats_highscores[j] = highscore[j]
                    game_stats[i] = f"{game}, {stats[1]}, {' '.join(map(lambda x: str(x) if x is not None else 'None', stats_highscores))}\n"
                    break
            # If game not found, add game to user
            else:
                games_stats.append(f"{game}, 1, {' '.join(map(lambda x: str(x) if x is not None else 'None', highscore))}\n")
            # Write updated stats to file
            file_lines[user_line_number] = "; ".join(games_stats)
            file.seek(0)
            file.writelines(file_lines)
    # If file does not exist, create file and write user and game stats
    except FileNotFoundError:
        try:
            with open("stats.txt", "w") as file:
                file.write(f"{active_account[0]}, {active_account[1]}\n" + f"    {game}, 1, {' '.join(map(lambda x: str(x) if x is not None else 'None', highscore))}\n")
        # If an error occurs while attempting to create the stats file, raise and print an exception
        except Exception as e:
            print(f"An error occurred while attempting to create the stats file: {e}")

def main():
    users = []
    try:
        with open("stats.txt", "r") as file:
            for line in file:
                user_info = line.strip().split("; ")
                retreived_player = user_info[0].strip().split(", ")
                users.append(Player(retreived_player[0], retreived_player[1]))
    except FileNotFoundError:
        with open("stats.txt", "w") as file:
            pass
    while True:
        active_account, signed_in = sign_in(users)
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