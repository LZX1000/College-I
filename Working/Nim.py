from Extras import yes_or_no, clear_screen, handle_value_error

#Prompts for and recieves the number of players, returning them as a list
def identify_players():
    #Initial print statement
    print("How many players are playing?\n")
    #Check for at least two players
    while True:
        num_players = handle_value_error()
        if num_players < 2:
            print("\nSorry but this game currently needs at least two players.\n")
        else:
            break
    #Initialize players []
    players = [f"Player{i+1}" for i in range(num_players)]
    #Return players and number of players
    return players, num_players

#Prints a custom prompt and returns `response` as either "y" or "n"
def try_again(current_player=None):
    if current_player == None:
        return main()
    #Get response
    print(f"{current_player} lost. Try again? (Y/N)\n")
    response = yes_or_no()
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
        start_nums.append(handle_value_error(f"{player}, choose a starting number: "))
    #Average starting numbers
    num_sums = sum(start_nums)
    starting_number = num_sums // len(players)
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
        if player_number <= 3:
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
        return main()
    game_number = choose_starting_number(players=players)
    #Return values
    return players, num_players, game_number

#Main loop
def main(players=None, num_players=0, game_number=0, current_player_index=0):
    #Starting functions
    clear_screen()
    players, num_players = identify_players()
    players, num_players, game_number = start(players=players, num_players=num_players)
    #Playing loop
    while True:
        #Ready turn
        player_choice = 0
        clear_screen()
        #Prompts and recieves integer choice from player
        current_player = players[current_player_index]
        player_choice = number_check(player_number=handle_value_error(f"There are currently {game_number} left.\n{current_player}, how many do you want to take?\n\n"), game_number=game_number, current_player=current_player)
        #Check for game over
        if player_choice >= game_number:
            response = try_again(current_player=current_player)
            #Play again or quit
            if response == "y":
                players, num_players, game_number = start(players=players, num_players=num_players)
            elif response == "n":
                break
        #Game continues
        else:
            game_number -= player_choice
            current_player_index = (current_player_index + 1) % num_players
    #End of game
    return
    
if __name__ == "__main__":
    main()