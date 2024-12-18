import random, keyboard, time
from Extras import Player, clear_screen, multiple_choice

def main(active_user=Player("Guest", "")):
    active = True
    while active ==True:
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
                response = multiple_choice("Are you sure you want to quit?")
                if response == "y":
                    active = False
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
        #Object starting positions
        starting_position = (random.randint(0, map_height-1), random.randint(0, map_width-1))
        for i in range(enemy_count):
            while True:
                enemy = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                if enemy != starting_position and enemy not in enemies:
                    enemies.append(enemy)
                    break
        for i in range(sword_pieces):
            while True:
                sword = (random.randint(0, map_height-1), random.randint(0, map_width-1))
                if sword != starting_position and sword not in enemies and sword not in pieces:
                    pieces.append(sword)
                    break
        #Display initial map
        game_map = [['x' for _ in range(map_width)] for _ in range(map_height)]
        game_map[starting_position[0]][starting_position[1]] = 'o'
        player_position = [starting_position[0], starting_position[1]]
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
                    response = multiple_choice("Are you sure you want to quit?")
                    if response == "y":
                        active = False
                    elif response == "n":
                        break
                #Movement
                if keyboard.is_pressed('w') or keyboard.is_pressed('up') or keyboard.is_pressed('8'):
                    if player_position[0]-1 in range(map_height):    
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0]-1, player_position[1]]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
                    else:
                        time.sleep(0.2)
                        break
                elif keyboard.is_pressed('s') or keyboard.is_pressed('down') or keyboard.is_pressed('2'):
                    if player_position[0]+1 in range(map_height):
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0]+1, player_position[1]]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
                    else:
                        time.sleep(0.2)
                        break
                elif keyboard.is_pressed('a') or keyboard.is_pressed('left') or keyboard.is_pressed('4'):
                    if player_position[1]-1 in range(map_width):
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0], player_position[1]-1]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
                    else:
                        time.sleep(0.2)
                        break
                elif keyboard.is_pressed('d') or keyboard.is_pressed('right') or keyboard.is_pressed('6'):
                    if player_position[1]+1 in range(map_width):
                        game_map[player_position[0]][player_position[1]] = ' '
                        player_position = [player_position[0], player_position[1]+1]
                        game_map[player_position[0]][player_position[1]] = 'o'
                        time.sleep(0.2)
                        break
        #Try again?
        response = multiple_choice("Would you like to play again?")
        if response == "n":
            active = False
        if response == "y":
            continue
    return 'The Arena', active_user, None

if __name__ == "__main__":
    main()