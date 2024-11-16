import random, time, keyboard
from Extras import clear_screen, yes_or_no

def main(active_user='Guest', map_width=16, map_height=16, max_apples=3):
    while True:
        temp_movement = None
        movement = None
        snake_length = 1
        player_position = [(map_height//2, map_width//2)]
        apples = []
        old = []
        game_map = [['\033[47m  \033[0m' for _ in range(map_width)] for _ in range(map_height)]
        previous_map = [['\033[37m  \033[0m' for _ in range(map_width)] for _ in range(map_height)]
        clear_screen()

        for _ in range(max_apples):
            while True:
                apple_position = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                if apple_position != player_position[0] and apple_position not in apples:
                    apples.append(apple_position)
                    break

        game_map[player_position[0][0]][player_position[0][1]] = '\033[32m██\033[0m'

        start_time = time.monotonic()
        while True:
            if player_position[0] in apples:
                snake_length += 1
                apples.remove(player_position[0])
                while True:
                    apple_position = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                    if apple_position not in player_position and apple_position not in apples:
                        apples.append(apple_position)
                        break

            points = snake_length - 1
            print(f"\033[1;1HPoints: {points}\n")

            for apple in apples:
                game_map[apple[0]][apple[1]] = '\033[47m🍎\033[0m'
            for y in range(map_height):
                for x in range(map_width):
                    if game_map[y][x] != previous_map[y][x]:
                        print(f"\033[{y+3};{x*2+1}H{game_map[y][x]}", end='')
            previous_map = [row[:] for row in game_map]
            print(f"\33[{map_height+3};0H", end='', flush=True)

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

            end_time = time.monotonic()
            if start_time == None or end_time-start_time >= 0.15:
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

                player_position.insert(0, new_head)
                if len(player_position) > snake_length:
                    tail = player_position.pop()
                    game_map[tail[0]][tail[1]] = '\033[47m██\033[0m'
                    old.append(tail)
                    if len(old) > 5:
                        old_pop = old.pop(0)
                        if old_pop in player_position:
                            game_map[old_pop[0]][old_pop[1]] = '\033[32m██\033[0m'
                        else:
                            game_map[old_pop[0]][old_pop[1]] = '\033[47m  \033[0m'

                game_map[player_position[0][0]][player_position[0][1]] = '\033[32m██\033[0m'

        # Try again?
        clear_screen("Game Over\n")
        try:
            if points > high_points:
                high_points = points
        except NameError:
            high_points = points
        response = yes_or_no("Would you like to play again? (Y/N)\n")
        if response == "n":
            return 'snake', high_points
        if response == "y":
            continue

if __name__ == "__main__":
    main()