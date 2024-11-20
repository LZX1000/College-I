from Extras import yes_or_no, clear_screen, handle_value_error
#Imports randint from random when it needs it later

#Prompts for and recieves the number of players, returning them as a list
def identify_players():
    #Initial print statement
    while True:
        num_players = handle_value_error("How many players are playing?\n")
        if num_players < 1:
            clear_screen("This game requires at least 1 player.\n")
        else:
            break
    #Initialize players []
    players = [f"Player{i+1}" for i in range(num_players)]
    if len(players) == 1:
        players.append("Robot")
        num_players += 1
    #Return players and number of players
    return players, num_players

#Prints a custom prompt and returns `response` as either "y" or "n"
def try_again(current_player=None):
    if current_player == None:
        return main()
    #Get response
    response = yes_or_no(f"{current_player} lost. Try again? (Y/N)\n")
    #Play again or quit
    if response == "y":
        clear_screen()
        return response
    elif response == "n":
        return response

#Prompts for and recieves a starting number from each player, returning the average as an integer
def choose_starting_number(players=None):
    #Initialize/check variables
    if players == None:
        return main()
    start_nums = []
    clear_screen()
    #All players choose a starting number
    for player in players:
        if player == "Robot":
            continue
        else:
            start_nums.append(handle_value_error(f"{player}, choose a starting number: "))
    #Average starting numbers
    num_sums = sum(start_nums)
    if "Robot" not in [players for players in players]:
        starting_number = num_sums // len(players)
    else:
        starting_number = num_sums
    print(f"\nThe starting number is {starting_number}.\n")
    #Return values
    return starting_number

#Checks that the number is within the games bounds, repeating until it is
def number_check(player_number=None, game_number=None, current_player=None):
    #Initialize/check variables
    if player_number == None or game_number == None or current_player == None:
        return main()
    condition = False
    #Get proper number loop
    while True:
        if player_number <= 3 and player_number >= 1:
            return player_number
        elif condition == True:
            clear_screen()
            player_number = handle_value_error(f"There are currently {game_number} left.\n{current_player}, how many do you want to take?\n\n{player_number}\n\nPlease choose an integer between 1 and 3.\n\n")
        else:
            player_number = handle_value_error("\nPlease choose an integer between 1 and 3.\n\n")
            condition = True

#Start the game with the given players and number of players
def start(players=None, num_players=None):
    #Check variables
    if players == None or num_players == None:
        players, num_players = identify_players()
    game_number = choose_starting_number(players=players)
    #Return values
    return players, num_players, game_number

#Prompt for and recieve the player's number
def get_player_choice(game_number=None, current_player=None):
    #Check/initialize variables
    if game_number == None or current_player == None:
        return main()
    #Get player number
    player_choice = number_check(handle_value_error(f"There are currently {game_number} left.\n{current_player}, how many do you want to take?\n\n"), game_number=game_number, current_player=current_player)
    return player_choice

#Generate random number from robot
def get_robot_choice():
    while True:
        try:
            return randint(1,3)
        except NameError:
            from random import randint

#Main loop
def main(active_user='Guest', players=None, num_players=0, game_number=0, current_player_index=0, current_player=None):
    game = True
    while game == True:
        #Starting functions
        clear_screen()
        current_player_index = 0
        players, num_players, game_number = start(players=players, num_players=num_players)
        if game_number == 0:
            game_number = choose_starting_number(players=players)
        #Game loop
        playing = True
        while playing == True:
            #Ready turn
            player_choice = 0
            clear_screen()
            #Prompts and recieves integer choice from player
            current_player = players[current_player_index]
            if current_player == "Robot":
                player_choice = get_robot_choice()
            else:
                player_choice = get_player_choice(game_number=game_number, current_player=current_player)
            #Check for game over
            if player_choice >= game_number:
                response = try_again(current_player=current_player)
                #Play again or quit
                if response == "y":
                    playing = False
                    break
                elif response == "n":
                    playing = game = False
                    break
            #Game continues
            else:
                game_number -= player_choice
                current_player_index = (current_player_index + 1) % num_players
    #End of game
    return 'Nim', active_user
    
if __name__ == "__main__":
    main()