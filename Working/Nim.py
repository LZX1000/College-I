#Imports

from Extras import yes_or_no, clear_screen, handle_value_error

#Players

def identify_players():
    print("How many players are playing?\n")
    num_players = handle_value_error()
    players = [f"Player{i+1}" for i in range(num_players)]

    return players, num_players

#Try again?

def try_again(current_player, players, num_players):
    print(f"{current_player} lost. Try again? (Y/N)\n")
    response = yes_or_no()

    if response == "y":
        clear_screen()
        play_again(players, num_players)
    elif response == "n":
        exit()

#Choosing a starting number by averaging the two numbers chosen by the players

def choose_starting_number(players = []):
    start_nums = []

    clear_screen()

    for player in players:
        print(f"{player}, choose a starting number: ")
        start_nums.append(handle_value_error())

    num_sums = sum(start_nums)
    starting_number = num_sums // len(players)

    print(f"\nThe starting number is {starting_number}.\n")
    
    return starting_number

#Check if it's a valid number (Between 1 and 3)

def number_check(player_number):
    if player_number <= 3:
        return player_number
    else:
        print("\nPlease choose an integer between 1 and 3.\n")
        player_number = handle_value_error()
        return number_check(player_number)

#Game loop

def game(players, num_players, game_number, current_player_index):
    player_choice = 0
    
    clear_screen()

    current_player = players[current_player_index]
    print(f"There are currently {game_number} left.\n{current_player}, how many do you want to take?\n")
    player_choice = number_check(player_number=handle_value_error())

    if player_choice >= game_number:
        try_again(current_player, players, num_players)
    else:
        game_number -= player_choice
        current_player_index = (current_player_index + 1) % num_players
        return game(players, num_players, game_number, current_player_index)

#Play again with the same players

def play_again(players, num_players):
    game_number = choose_starting_number(players)
    current_player_index = 0

    game(players, num_players, game_number, current_player_index)

#Main loop

def main():
    clear_screen()

    players, num_players = identify_players()

    play_again(players, num_players)
if __name__ == "__main__":
    main()