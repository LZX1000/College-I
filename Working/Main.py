from Nim import main as nim
from Word_Guess import main as word_guess
from Extras import clear_screen

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
    while True:
        #Defines the games in the menu as a list
        menu = ["Quit", "Nim", "Word Guess"]
        clear_screen()
        #Gets a proper input and runs the menu item associated with it
        eval((check_menu_choice(menu, "Which game would you like to play?\n\n" + "\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]) + "\n\n").strip().lower().replace(" ", "_") + '()'))

if __name__ == "__main__":
    main()