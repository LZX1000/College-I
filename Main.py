from Nim import main as nim
from Word_Guess import main as word_guess
from The_Arena import main as the_arena
from Snake import main as snake
from Extras import clear_screen, yes_or_no
from Start import main as start_main

def sign_in():
    """
    Handles the sign-in process for users.

    This function clears the screen and prompts the user to either sign in with an existing account
    or create a new one. If the user chooses to sign in, they are asked for their username and password.
    If the credentials match an existing user, they are welcomed. If the credentials do not match,
    an error message is displayed. If the user chooses to create a new account, they are prompted to
    enter a new username and password. The new account is then saved to the "users.txt" file.

    Returns:
        str: The username of the signed-in or newly created user.
    """
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
                return username_try
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
                    return new_user

#Check if the choice is in the menu
def check_menu_choice(menu, prompt=''):
    while True:
        choice = input(prompt)
        #Check if the choice is in the menu as an integer
        try:
            if int(choice) in range(len(menu)):
                return menu[int(choice)]
        #check if the choice is in the menu as a string
        except ValueError:
            if choice.strip().lower().replace(" ", "_") in [item.strip().lower().replace(" ", "_") for item in menu]:
                return choice
        #If the choice is not in the menu, ask for a new choice, suggesting the user inputs an integer
        clear_screen("Invalid choice.")

#Main function
def main():
    active_user = sign_in()
    while True:
        #Defines the games in the menu as a list
        menu = ["Quit", "Nim", "Word Guess", "The Arena", "Snake"]
        clear_screen()
        #Gets a proper input and runs the menu item associated with it
        game, score = eval((check_menu_choice(menu, "Which game would you like to play?\n\n" + "\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]) + "\n\n").strip().lower().replace(" ", "_") + '(active_user=active_user)'))

if __name__ == "__main__":
    main()