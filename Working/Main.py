from Nim import main as nim
from Word_Guess import main as word_guess
from Extras import clear_screen, yes_or_no

def sign_in():
    clear_screen()
    while True:
        #Check if there is a users file yet
        try:
            with open("users.txt", "r") as file:
                users = [tuple(line.strip().split(', ')) for line in file.readlines()]
        except FileNotFoundError:
            with open("users.txt", "w") as file:
                users = []
        response = yes_or_no("Do you already have an account? (Y/N)\n\n")
        #If the user has an account
        if response == "y":
            #Get and check username and password
            clear_screen()
            username_try = input("Username: ")
            password_try = input("\nPassword: ")
            attempt = (username_try, password_try)
            if attempt in users:
                clear_screen(f"Welcome, {username_try}!")
                return username_try
            else:
                clear_screen("Invalid username or password.")
        #If the user doesn't have an account
        elif response == "n":
            clear_screen("What should we call you?\n")
            new_user = input("Username: ")
            while True:
                if any(new_user == user[0] for user in users):
                    clear_screen("That username is already taken.\n")
                    new_user = input("\nPlease enter something else\n" + "\nUsername: ")
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
        menu = ["Quit", "Nim", "Word Guess"]
        clear_screen()
        #Gets a proper input and runs the menu item associated with it
        eval((check_menu_choice(menu, "Which game would you like to play?\n\n" + "\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]) + "\n\n").strip().lower().replace(" ", "_") + '(active_user=active_user)'))

if __name__ == "__main__":
    main()