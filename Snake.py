import random, keyboard, time
from Extras import clear_screen, yes_or_no, handle_value_error

def main(active_user='Guest'):
    while True:
        clear_screen()
        movement = None
        snake_length = 1
        max_apples = 3
        apples = []

        # map_width = handle_value_error("Map width: ")
        # map_height = handle_value_error("Map height: ")
        map_width = 20
        map_height = 20

        game_map = [['██' for _ in range(map_width)] for _ in range(map_height)]
        previous_map = [['██' for _ in range(map_width)] for _ in range(map_height)]

        player_position = [(random.randint(0, map_height-1), random.randint(0, map_width-1))]
        for i in range(max_apples):
            while True:
                apple_position = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                if apple_position != player_position[0] and apple_position not in apples:
                    apples.append(apple_position)
                    break

        game_map[player_position[0][0]][player_position[0][1]] = '  '
        #Print initial game map
        for apple in apples:
            game_map[apple[0]][apple[1]] = '🍎'
        for y in range(map_height):
            for x in range(map_width):
                if game_map[y][x] != previous_map[y][x]:
                    print(f"\033[{y+1};{x*2+1}H{game_map[y][x]}", end='')
        previous_map = [row[:] for row in game_map]

        while True:
            if player_position[0] in apples:
                snake_length += 1
                apples.remove(player_position[0])
                while True:
                    apple_position = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                    if apple_position != player_position[0] and apple_position not in apples:
                        apples.append(apple_position)
                        break

            for apple in apples:
                game_map[apple[0]][apple[1]] = '🍎'
            for y in range(map_height):
                for x in range(map_width):
                    if game_map[y][x] != previous_map[y][x]:
                        print(f"\033[{y+1};{x*2+1}H{game_map[y][x]}", end='')
            previous_map = [row[:] for row in game_map]

            if keyboard.is_pressed('w') or keyboard.is_pressed('up') and movement != 'down':
                movement = 'up'
            elif keyboard.is_pressed('s') or keyboard.is_pressed('down') and movement != 'up':
                movement = 'down'
            elif keyboard.is_pressed('a') or keyboard.is_pressed('left') and movement != 'right':
                movement = 'left'
            elif keyboard.is_pressed('d') or keyboard.is_pressed('right') and movement != 'left':
                movement = 'right'

            if movement == 'up':
                if player_position[0][0]-1 in range(map_height):
                    new_head = (player_position[0][0]-1, player_position[0][1])
                else:
                     break
            elif movement == 'down':
                if player_position[0][0]+1 in range(map_height):
                    new_head = (player_position[0][0]+1, player_position[0][1])
                else:
                    break
            elif movement == 'left':
                if player_position[0][1]-1 in range(map_width):
                    new_head = (player_position[0][0], player_position[0][1]-1)
                else:
                    break
            elif movement == 'right':
                if player_position[0][1]+1 in range(map_width):
                    new_head = (player_position[0][0], player_position[0][1]+1)
                else:
                    break
            else:
                continue

            player_position.insert(0, new_head)
            if len(player_position) > snake_length:
                tail = player_position.pop()
                game_map[tail[0]][tail[1]] = '██'

            game_map[player_position[0][0]][player_position[0][1]] = '  '

            time.sleep(0.2)
        #Try again?
        clear_screen("Game Over\n")
        response = yes_or_no("Would you like to play again? (Y/N)\n")
        if response == "n":
            return
        if response == "y":
            continue

if __name__ == "__main__":
    main()

'''
Modify this code to make snake later
'''