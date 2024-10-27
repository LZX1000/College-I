from Nim import main as nim
from Word_Guess import main as word_guess
from Extras import handle_value_error, clear_screen

#Check if the choice is in the menu
def check_menu_choice(menu=[], choice=None):
    #Check that parameters are valid
    if menu == []:
        return main()
    if choice == None:
        choice = input()
    #Check if the choice is in the menu as an integer
    if choice in range(len(menu)):
        return menu[choice]
    #check if the choice is in the menu as a string
    elif choice.strip().lower().replace(" ", "_") in [item.strip().lower().replace(" ", "_") for item in menu]:
        return choice
    #If the choice is not in the menu, ask for a new choice, suggesting the user inputs an intiger
    else:
        print("Invalid choice.")
        choice = handle_value_error()
        return check_menu_choice(menu, choice=choice)

#Main function
def main():
    #Defines the games in the menu as a list
    menu = ["Quit", "Nim", "Word Guess"]
    clear_screen()
    #Asks the user to choose a game, printing the games in the menu
    print("Which game would you like to play?\n")
    print("\n".join([f"{index} : {menu[index]}" for index in range(len(menu))]))
    #Checks the choice for the corresponding name or index in menu[]
    choice_name = (check_menu_choice(menu).strip().lower()).replace(" ", "_")
    #Evaluates the choice to call the corresponding game function
    eval((choice_name + '()'))

if __name__ == "__main__":
    main()