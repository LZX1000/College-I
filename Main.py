from Nim import main as nim
from Word_Guess import main as word_guess
from The_Arena import main as the_arena
from Snake import main as snake
from Number_Guess import main as number_guess
from Extras import clear_screen, yes_or_no, check_menu_choice
from Start import main as start_main

def sign_in():
    '''
    Handles the sign-in process for users.

    This function clears the screen and prompts the user to either sign in with an existing account
    or create a new one. If the user chooses to sign in, they are asked for their username and password.
    If the credentials match an existing user, they are welcomed. If the credentials do not match,
    an error message is displayed. If the user chooses to create a new account, they are prompted to
    enter a new username and password. The new account is then saved to the "users.txt" file.

    Returns:
        str: The username of the signed-in or newly created user.
    '''
    clear_screen()
    while True:
        #Open existing users file or create a new one
        try:
            with open("users.txt", "r") as file:
                users = [tuple(line.strip().split(', ')) for line in file.readlines()]
        except FileNotFoundError:
            with open("users.txt", "w") as file:
                users = []
        response = yes_or_no("Do you already have an account? (Y/N)\n\n")
        #Sign in
        if response == "y":
            clear_screen()
            username_try = input("Username: ")
            password_try = input("\nPassword: ")
            attempt = (username_try, password_try)
            if attempt in users:
                #Correct credentials
                clear_screen(f"Welcome, {username_try}!")
                return username_try, True
            else:
                #To the beginning of the loop
                clear_screen("Invalid username or password.")
        #Create new account
        elif response == "n":
            clear_screen("What should we call you?\n")
            new_user = input("Username: ")
            while True:
                #Check if it's a taken username
                if any(new_user == user[0] for user in users):
                    clear_screen("That username is already taken.\nWould you like to sign in? (Y/N)\n")
                    response = yes_or_no()
                    if response == "y":
                        clear_screen()
                        break
                    elif response == "n":
                        clear_screen()
                        new_user = input("Username: ")
                #Not taken, make a password
                else:
                    new_pass = input("\nPassword: ")
                    users.append((new_user, new_pass))
                    with open("users.txt", "a") as file:
                        file.write(f"{new_user}, {new_pass}\n")
                    return new_user, True

def unpack_game(game, active_user, highscore=[]):
    try:
        main_line = None
        sublines = []
        with open("stats.txt", "r+") as file:
            while user_found is False:
                for i, line in enumerate(file):
                    if active_user in line:
                        user_found = True
                        main_line = line
                        main_line_number = i
                if user_found is False:
                    file.write(f"{active_user}\n    ")
                for subline in file[main_line_number + 1:]:
                    if len(subline) - len(subline.lstrip()) > len(main_line) - len(main_line.lstrip()):
                        sublines.append(subline)
                    else:
                        break
            for i, subline in enumerate(sublines):
                if game in subline:
                    stats = subline.strip().split(", ")
                    stats[1] = str(int(stats[1]) + 1)
                    stats_highscores = stats[2].split(" ")
                    for i, stats_highscore in enumerate(stats_highscores):
                        if highscore[i] > int(stats_highscore):
                            stats_highscores[i] = highscore[i]
                    sublines[i] = f"{game}, {stats[1]}, {' '.join(stats_highscores)}\n"
                    break
            else:
                sublines.append(f"{game}, 1, {' '.join(map(str, highscore))}\n")
            file.seek(0)
            for line in file:
                if line in sublines:
                    file.write(line)
    except FileNotFoundError:
        with open("stats.txt", "w") as file:
            file.write(f"{active_user}\n" + f"    {game}, 1, {' '.join(map(str, highscore))}\n")

#Main function
def main():
    while True:
        active_user, signed_in = sign_in()
        while signed_in == True:
            #Defines the games in the menu as a list
            menu = ["Quit", "Sign Out", "Nim", "Number Guess", "Word Guess", "The Arena", "Snake"]
            clear_screen()
            #Gets a proper input and runs the menu item associated with it
            unpack_game(eval(check_menu_choice(menu, "Which game would you like to play?\n\n" + "\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]) + "\n\n").strip().lower().replace(" ", "_") + '(active_user=active_user)'))

if __name__ == "__main__":
    main()