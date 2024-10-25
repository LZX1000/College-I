#Players

NUM_PLAYERS = 2
players = [f"Player{i+1}" for i in range(NUM_PLAYERS)]

#Clear screen

def clear_screen():
    print("\n" * 50)

#Handling ValueError

def handle_value_error():
    while True:
        try:
            return int(input())
        except ValueError:
            print("\nPlease enter a valid integer.\n")

#Try again?

def try_again():
    print(f"{CURRENT_PLAYER} lost. Try again? (Y/N)\n")
    while True:
        response = input().lower()

        if response == "y":
            clear_screen()
            nim()
        elif response == "n":
            exit()
        else:
            print('\nPlease enter "Y" or "N".\n')



#Choosing a starting number by averaging the two numbers chosen by the players

def choose_starting_number():
    start_nums = []

    for player in players:
        print(f"{player}, choose a starting number: ")
        start_nums.append(handle_value_error())

    num_sums = sum(start_nums)
    starting_number = num_sums // len(players)

    print(f"\nThe starting number is {starting_number}.\n")
    
    return starting_number

#Game loop

def nim():
    global CURRENT_PLAYER

    game_number = choose_starting_number()
    current_player_index = 0
    player_choice = 0

    while True:
        CURRENT_PLAYER = players[current_player_index]
        print(f"\n\nThere are currently {game_number} left.\n{CURRENT_PLAYER}, how many do you want to take?\n")
        player_choice = handle_value_error()

        while True:
            if player_choice <= 3:
                if player_choice >= game_number:
                    try_again()
                    break
                else:
                    game_number -= player_choice
                    break
            else:
                print("\nPlease choose a number between 1 and 3.\n")
                player_choice = handle_value_error()
    
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    nim()