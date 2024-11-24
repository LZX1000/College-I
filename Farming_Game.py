import random, time, keyboard
from Extras import clear_screen, yes_or_no

def main(active_user='Guest'):
    map_width = 16
    map_height = 16
    movement_time = 0.15
    while True:
        # Initialize game specific variables
        player_position = (map_height//2, map_width//2)
        game_map = [['\033[47m  \033[0m' for _ in range(map_width)] for _ in range(map_height)]
        previous_map = [['\033[37m  \033[0m' for _ in range(map_width)] for _ in range(map_height)]
        clear_screen()
        # Display initial player head
        game_map[player_position[0]][player_position[1]] = '\033[93m██\033[0m'
        # Game start time
        start_time = time.monotonic()
        # Game loop
        while True:
            print("\033[1;1HPoints: {points}\n")
            # Display game map
            for y in range(map_height):
                for x in range(map_width):
                    if game_map[y][x] != previous_map[y][x]:
                        print(f"\033[{y+3};{x*2+1}H{game_map[y][x]}", end='')
            previous_map = [row[:] for row in game_map]
            print(f"\33[{map_height+3};0H", end='', flush=True)
            # Check for movement inputs
            while True:
                old_position = None
                if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                    if end_time-start_time >= movement_time or start_time is None:
                        start_time = time.monotonic()
                        if player_position[0]-1 in range(map_height) and (player_position[0]-1, player_position[1]) not in player_position:
                            old_position = player_position
                            player_position = (player_position[0]-1, player_position[1])
                            break
                elif keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                    if end_time-start_time >= movement_time or start_time is None:
                        start_time = time.monotonic()
                        if player_position[0]+1 in range(map_height) and (player_position[0]+1, player_position[1]) not in player_position:
                            old_position = player_position
                            player_position = (player_position[0]+1, player_position[1])
                            break
                elif keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                    if end_time-start_time >= movement_time or start_time is None:
                        start_time = time.monotonic()
                        if player_position[1]-1 in range(map_width) and (player_position[0], player_position[1]-1) not in player_position:
                            old_position = player_position
                            player_position = (player_position[0], player_position[1]-1)
                            break
                elif keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                    if end_time-start_time >= movement_time or start_time is None:
                        start_time = time.monotonic()
                        if player_position[1]+1 in range(map_width) and (player_position[0], player_position[1]+1) not in player_position:
                            old_position = player_position
                            player_position = (player_position[0], player_position[1]+1)
                            break
                # Handle movement if enough time has passed
                end_time = time.monotonic()
            # Update player position and handle trail
            game_map[old_position[0]][old_position[1]] = '\033[47m  \033[0m'
            game_map[player_position[0]][player_position[1]] = '\033[93m██\033[0m'
        # Game over
        clear_screen("Game Over")
        # Play again
        response = yes_or_no("\nWould you like to play again? (Y/N)\n")
        if response == "n":
            return 'Snake', active_user, None
        if response == "y":
            continue

if __name__ == "__main__":
    main()