import random, keyboard, time
from Extras import clear_screen, yes_or_no

def main(active_user='Guest'):
    while True:
        enemies = []
        pieces = []
        pieces_collected = 0
        clear_screen()
        #Set difficulty loop
        while True:
            difficulty = input("Select a difficulty!\n" + "1: Easy\n" + "2: Medium\n" + "3: Hard\n\n").lower().strip()
            #Check quit
            if keyboard.is_pressed('esc'):
                clear_screen()
                response = yes_or_no("Are you sure you want to quit? (Y/N)\n")
                if response == "y":
                    return
                elif response == "n":
                    continue
            #Difficulty sets
            if difficulty == '1' or difficulty == 'easy':
                enemy_count = 1
                sword_pieces = 5
                needed_sword_pieces = 3
                map_width, map_height = 5, 5
                break
            elif difficulty == '2' or difficulty == 'medium':
                enemy_count = 3
                sword_pieces = 4
                needed_sword_pieces = 3
                map_width, map_height = 7, 7
                break
            elif difficulty == '3' or difficulty == 'hard':
                enemy_count = 5
                sword_pieces = 3
                needed_sword_pieces = 3
                map_width, map_height = 10, 10
                break
            else:
                clear_screen("Please select a valid difficulty!\n\n")
        #Player starting position
        starting_y = random.randint(0, map_height-1)
        starting_x = random.randint(0, map_width-1)
        #Enemy starting positions
        for i in range(enemy_count):
            enemy_y = random.randint(0, map_height-1)
            enemy_x = random.randint(0, map_width-1)
            if (enemy_y, enemy_x) != (starting_y, starting_x) and (enemy_x, enemy_y) not in enemies:
                enemies.append((enemy_y, enemy_x))
                break
        #Sword pieces starting positions
        for i in range(sword_pieces):
            sword_y = random.randint(0, map_height-1)
            sword_x = random.randint(0, map_width-1)
            if (sword_y, sword_x) != (starting_y, starting_x) and (sword_y, sword_x) not in enemies and (sword_y, sword_x) not in pieces:
                pieces.append((sword_y, sword_x))
        #Display initial map
        game_map = [['x' for _ in range(map_width)] for _ in range(map_height)]
        game_map[starting_y][starting_x] = 'o'
        player_position = [starting_y, starting_x]
        #Game loop
        while True:
            #Display game
            clear_screen(f"Pieces collected: {pieces_collected}/{needed_sword_pieces}\n")
            for row in game_map:
                print(' '.join(row))
            #Check if the player is on a non-blank tile
            if tuple(player_position) in enemies:
                if pieces_collected >= needed_sword_pieces:
                    clear_screen("Congratulations! You have collected all the pieces and defeated the enemy!\n")
                    break
                else:
                    clear_screen("You could not assemble your sword before you found the enemy.\n")
                    break
            elif tuple(player_position) in pieces and pieces_collected < needed_sword_pieces:
                if pieces_collected < needed_sword_pieces:
                    pieces_collected += 1
            #Keyboard input loop
            while True:
                #Check quit
                if keyboard.is_pressed('esc'):
                    clear_screen()
                    response = yes_or_no("Are you sure you want to quit? (Y/N)\n")
                    if response == "y":
                        return
                    elif response == "n":
                        break
                #Movement
                if keyboard.is_pressed('w') or keyboard.is_pressed('up') or keyboard.is_pressed('u') or keyboard.is_pressed('8'):
                    if player_position[0]-1 in range(map_height):    
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0]-1, player_position[1]]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
                    else:
                        time.sleep(0.2)
                        break
                elif keyboard.is_pressed('s') or keyboard.is_pressed('down') or keyboard.is_pressed('d') or keyboard.is_pressed('2'):
                    if player_position[0]+1 in range(map_height):
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0]+1, player_position[1]]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
                    else:
                        time.sleep(0.2)
                        break
                elif keyboard.is_pressed('a') or keyboard.is_pressed('left') or keyboard.is_pressed('l') or keyboard.is_pressed('4'):
                    if player_position[1]-1 in range(map_width):
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0], player_position[1]-1]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
                    else:
                        time.sleep(0.2)
                        break
                elif keyboard.is_pressed('d') or keyboard.is_pressed('right') or keyboard.is_pressed('r') or keyboard.is_pressed('6'):
                    if player_position[1]+1 in range(map_width):
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0], player_position[1]+1]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
        #Try again?
        response = yes_or_no("Would you like to play again? (Y/N)\n")
        if response == "n":
            return
        if response == "y":
            continue

if __name__ == "__main__":
    main()