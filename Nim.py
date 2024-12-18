from Extras import Player, multiple_choice, clear_screen, handle_value
from random import randint

def main(active_user=Player("Guest", "")):
    """
    Main function to run the Nim game.

    Parameters:
    active_user (str): The name of the active user. Default is 'Guest'.

    Returns:
    tuple: A tuple containing the game name 'Nim', the active user, and None.
    """
    clear_screen()
    # Get player count
    while True:
        num_players = handle_value("How many players are playing?\n")
        if num_players < 1:
            clear_screen("This game requires at least 1 player.\n")
        else:
            break
    # Prep players list
    players = [f"Player{i+1}" for i in range(num_players)]
    players[0] = active_user.username
    if len(players) == 1:
        players.append("Robot")
        num_players += 1
    # Game loop
    while True:
        clear_screen()
        start_nums = []
        # Get starting numbers
        for player in players:
            if player == "Robot":
                continue
            else:
                while True:
                    start_choice = handle_value(f"{player}, choose a starting number: ")
                    if start_choice < 1:
                        clear_screen("Please choose a positive integer.\n")
                    else:
                        start_nums.append(start_choice)
                        break
        num_sums = sum(start_nums)
        # Average starting numbers
        if "Robot" not in [players for players in players]:
            game_number = num_sums // len(players)
        else:
            game_number = num_sums
        print(f"\nThe starting number is {game_number}.\n")
        current_player_index = 0
        player_choice = False
        # Playing loop
        while True:
            clear_screen()
            if player_choice:
                print(f"{players[(current_player_index - 1) % num_players]} took {player_choice} from the pile.\n")
            current_player = players[current_player_index]
            player_choice = 0
            # Get choices
            if current_player == "Robot":
                for i in range(1, 4):
                    if (game_number - i) % 4 == 1:
                        player_choice = i
                        break
                    else:
                        player_choice = randint(1, 3)
            else:
                player_choice = handle_value(f"There are currently {game_number} left.\n{current_player}, how many do you want to take?\n\n")
                condition = False
                while True:
                    if player_choice <= 3 and player_choice >= 1:
                        break
                    elif condition == True:
                        clear_screen()
                        player_choice = handle_value("Please choose an integer between 1 and 3.\n\n" + f"There are currently {game_number} left." + f"\n{current_player}, how many do you want to take?\n\n")
                    else:
                        condition = True
            # Evaluate choice
            if player_choice >= game_number:
                response = multiple_choice(f"{current_player} lost. Try again?")
                break
            else:
                game_number -= player_choice
                current_player_index = (current_player_index + 1) % num_players
        # Quit
        if response == "n":
            break
    return 'Nim', active_user, None
    
if __name__ == "__main__":
    main()