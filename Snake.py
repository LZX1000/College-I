import random, time, keyboard
from Extras import Player, clear_screen, yes_or_no

def main(active_user=Player("Guest", "")):
    '''
    Main function to run the Snake game.

    Parameters:
    active_user (str): The name of the active user playing the game. Default is 'Guest'.
    high_points (int): The current high score for the game. Default is 0.
    map_width (int): The width of the game map. Default is 16.
    map_height (int): The height of the game map. Default is 16.
    max_apples (int): The maximum number of apples that can appear on the map at once. Default is 3.

    Returns:
    tuple: A tuple containing the string 'snake' and the high score achieved during the game.
    '''
    map_width = 16
    map_height = 16
    max_apples = 3
    # Get high_points
    try:
        with open("stats.txt", "r") as file:
            file_lines = file.readlines()
            main_line_number = None
            for i, line in enumerate(file_lines):
                if line.startswith(f"{active_user.username}, {active_user.password}"):
                    main_line = line
                    main_line_number = i
                    sublines = []
                    break
            if main_line_number is not None:
                for subline in file_lines[main_line_number + 1:]:
                    if len(subline) - len(subline.lstrip()) > len(main_line) - len(main_line.lstrip()):
                        sublines.append(subline)
                    else:
                        break
                for subline in sublines:
                    if "Snake" in subline:
                        stats = subline.strip().split(", ")
                        high_points = int(stats[2].split(" ")[0])
                        break
                else:
                    high_points = 0
            else:
                high_points = 0
    except (FileNotFoundError, UnboundLocalError):
        high_points = 0
    while True:
        # Initialize game specific variables
        temp_movement = None
        movement = None
        snake_length = 1
        player_position = [(map_height//2, map_width//2)]
        apples = []
        old = []
        game_map = [['\033[47m  \033[0m' for _ in range(map_width)] for _ in range(map_height)]
        previous_map = [['\033[37m  \033[0m' for _ in range(map_width)] for _ in range(map_height)]
        clear_screen()
        # Generate initial apples
        for _ in range(max_apples):
            while True:
                apple_position = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                if apple_position != player_position[0] and apple_position not in apples:
                    apples.append(apple_position)
                    break
        # Display initial player head
        game_map[player_position[0][0]][player_position[0][1]] = '\033[93m██\033[0m'
        # Game start time
        start_time = time.monotonic()
        # Game loop
        while True:
            # Handle apple collisions (generate new apple, increase snake length)
            if player_position[0] in apples:
                snake_length += 1
                apples.remove(player_position[0])
                while True:
                    apple_position = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                    if apple_position not in player_position and apple_position not in apples:
                        apples.append(apple_position)
                        break
            # Points
            points = snake_length - 1
            print(f"\033[1;1HPoints: {points}\n")
            # Display game map
            for apple in apples:
                if apple in old:
                    game_map[apple[0]][apple[1]] = '\033[32m🍎\033[0m'
                else:
                    game_map[apple[0]][apple[1]] = '\033[47m🍎\033[0m'
            for y in range(map_height):
                for x in range(map_width):
                    if game_map[y][x] != previous_map[y][x]:
                        print(f"\033[{y+3};{x*2+1}H{game_map[y][x]}", end='')
            previous_map = [row[:] for row in game_map]
            print(f"\33[{map_height+3};0H", end='', flush=True)
            # Check for movement inputs
            if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                if movement != 'down':
                    temp_movement = 'up'
            elif keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                if movement != 'up':
                    temp_movement = 'down'
            elif keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                if movement != 'right':
                    temp_movement = 'left'
            elif keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                if movement != 'left':
                    temp_movement = 'right'
            # Handle movement if enough time has passed
            end_time = time.monotonic()
            if start_time is None or end_time-start_time >= 0.15:
                start_time = time.monotonic()
                movement = temp_movement
                if movement == 'up':
                    if player_position[0][0]-1 in range(map_height) and (player_position[0][0]-1, player_position[0][1]) not in player_position:
                        new_head = (player_position[0][0]-1, player_position[0][1])
                    else:
                        break
                elif movement == 'down':
                    if player_position[0][0]+1 in range(map_height) and (player_position[0][0]+1, player_position[0][1]) not in player_position:
                        new_head = (player_position[0][0]+1, player_position[0][1])
                    else:
                        break
                elif movement == 'left':
                    if player_position[0][1]-1 in range(map_width) and (player_position[0][0], player_position[0][1]-1) not in player_position:
                        new_head = (player_position[0][0], player_position[0][1]-1)
                    else:
                        break
                elif movement == 'right':
                    if player_position[0][1]+1 in range(map_width) and (player_position[0][0], player_position[0][1]+1) not in player_position:
                        new_head = (player_position[0][0], player_position[0][1]+1)
                    else:
                        break
                else:
                    continue
                # Update player position and handle trail
                player_position.insert(0, new_head)
                if len(player_position) > snake_length:
                    tail = player_position.pop()
                    game_map[tail[0]][tail[1]] = '\033[247m██\033[0m'
                    old.append(tail)
                    if len(old) > 5:
                        old_pop = old.pop(0)
                        if old_pop in player_position:
                            game_map[old_pop[0]][old_pop[1]] = '\033[32m██\033[0m'
                        else:
                            game_map[old_pop[0]][old_pop[1]] = '\033[47m  \033[0m'
                # Snake colors
                for i in range(1, len(player_position)):
                    if (i // 2) % 2 == 0:
                        color = 32
                    else:
                        color = 92
                    game_map[player_position[i][0]][player_position[i][1]] = f'\033[{color}m██\033[0m'
                game_map[player_position[0][0]][player_position[0][1]] = '\033[93m██\033[0m'
        # Game over
        keyboard.send('enter')
        input()
        clear_screen("Game Over\n")
        # Update highscore
        if points > high_points:
            high_points = points
        print(f"Score: {points}             High Score: {high_points}")
        if points == high_points:
            print("\033[3m*New High Score!*\33[0m\n")
        else:
            print()
        # Play again
        response = yes_or_no("Would you like to play again? (Y/N)\n")
        if response == "n":
            return 'Snake', active_user, high_points
        if response == "y":
            continue

if __name__ == "__main__":
    main()