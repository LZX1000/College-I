from Nim import main as nim
from Word_Guess import main as word_guess
from Extras import handle_value_error, clear_screen

#Check if the choice is in the menu
def check_menu_choice(menu, choice=None):
    while True:
        #Check that parameters are valid
        if choice == None:
            choice = input()
        #Check if the choice is in the menu as an integer
        try:
            if int(choice) in range(len(menu)):
                return menu[int(choice)]
        #check if the choice is in the menu as a string
        except ValueError:
            if choice.strip().lower().replace(" ", "_") in [item.strip().lower().replace(" ", "_") for item in menu]:
                return choice
        #If the choice is not in the menu, ask for a new choice, suggesting the user inputs an integer
        print("Invalid choice.")
        choice = handle_value_error()

#Main function
def main():
    while True:
        #Defines the games in the menu as a list
        menu = ["Quit", "Nim", "Word Guess"]
        #Asks the user to choose a game, printing the games in the menu
        clear_screen("Which game would you like to play?\n\n" + "\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]) + "\n")
        #Checks the choice for the corresponding name or index in menu[]
        choice_name = check_menu_choice(menu).strip().lower().replace(" ", "_")
        #Evaluates the choice to call the corresponding game function
        eval((choice_name + '()'))

if __name__ == "__main__":
    main()