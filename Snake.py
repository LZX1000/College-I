import random, keyboard, time
from Extras import clear_screen, yes_or_no, handle_value_error

def main(active_user='Guest'):
    while True:
        clear_screen()
        movement = None
        snake_length = 1
        max_apples = 3
        apples = []

        map_width = handle_value_error("Map width: ")
        map_height = handle_value_error("Map height: ")

        game_map = [['██' for _ in range(map_width)] for _ in range(map_height)]

        player_position = [(random.randint(0, map_height-1), random.randint(0, map_width-1))]
        for i in range(max_apples):
            while True:
                apple_poition = [(random.randint(0, map_height-1), random.randint(0, map_width-1))]
                if apple_poition != player_position and apple_poition not in apples:
                    apples.append(apple_poition)
                    break

        game_map[player_position[0][0]][player_position[0][1]] = '  '

        while True:
            clear_screen()
            if player_position[0] in apples:
                snake_length += 1
                apples.remove(player_position[0])
                while True:
                    apple_poition = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                    if apple_poition != player_position and apple_poition not in apples:
                        apples.append(apple_poition)
                        break
            for apple in apples:
                game_map[apple[0][0]][apple[0][1]] = '🍎'
            for row in game_map:
                print(''.join(row))

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
                    game_map[player_position[0][0]][player_position[0][1]] = '██'
                    player_position[0] = (player_position[0][0]-1, player_position[0][1])
                    game_map[player_position[0][0]][player_position[0][1]] = '  '
                    time.sleep(0.2)
                else:
                     break
            elif movement == 'down':
                if player_position[0][0]+1 in range(map_height):
                    game_map[player_position[0][0]][player_position[0][1]] = '██'
                    player_position[0] = (player_position[0][0]+1, player_position[0][1])
                    game_map[player_position[0][0]][player_position[0][1]] = '  '
                    time.sleep(0.2)
                else:
                    break
            elif movement == 'left':
                if player_position[0][1]-1 in range(map_width):
                    game_map[player_position[0][0]][player_position[0][1]] = '██'
                    player_position[0] = (player_position[0][0], player_position[0][1]-1)
                    game_map[player_position[0][0]][player_position[0][1]] = '  '
                    time.sleep(0.2)
                else:
                    break
            elif movement == 'right':
                if player_position[0][1]+1 in range(map_width):
                    game_map[player_position[0][0]][player_position[0][1]] = '██'
                    player_position[0] = (player_position[0][0], player_position[0][1]+1)
                    game_map[player_position[0][0]][player_position[0][1]] = '  '
                    time.sleep(0.2)
                else:
                    break
            else:
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