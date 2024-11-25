import random, time, keyboard
from Extras import clear_screen, yes_or_no

def main(active_user='Guest'):
    map_width = 16
    map_height = 16
    movement_time = 0.15
    playing = True
    while playing:
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
            print(f"\033[{map_height+3};0H", end='', flush=True)
            # Check for movement inputs
            y_movement = 0
            x_movement = 0
            while True:
                if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                    y_movement = 1
                elif keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                    y_movement = -1
                if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                    x_movement = -1
                elif keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                    x_movement = 1
                if keyboard.is_pressed('esc'):
                    clear_screen()
                    pause_response = yes_or_no("Are you sure you want to quit? (Y/N)\n\n")
                    clear_screen()
                    if pause_response == "y":
                        playing = False
                        break
                    elif pause_response == "n":
                        previous_map = [['\033[37m  \033[0m' for _ in range(map_width)] for _ in range(map_height)]
                # Handle movement if enough time has passed
                end_time = time.monotonic()
                if end_time-start_time >= movement_time or start_time is None:
                    start_time = time.monotonic()
                    break
            old_position = (player_position[0]+y_movement, player_position[1]-x_movement)
            # Update player position and handle trail
            if old_position != player_position:
                color = random.choice(['\033[41m  \033[0m', '\033[42m  \033[0m', '\033[43m  \033[0m', '\033[44m  \033[0m', '\033[45m  \033[0m', '\033[46m  \033[0m'])
                game_map[old_position[0]][old_position[1]] = color
                for y in range(map_height):
                    for x in range(map_width):
                        game_map[y][x] = previous_map[y+y_movement][x-x_movement]
                        if game_map[y][x] not in range(map_height) or game_map[y][x] not in range(map_width):
                            # Make it so the map moves
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