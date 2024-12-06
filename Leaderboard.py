import keyboard
from Extras import check_menu_choice, clear_screen

def main():
    leaderboard_menu = ["Back", "Nim", "Number Guess", "Word Guess", "The Arena", "Snake"]
    playing = True

    try:
        with open("stats.txt", "r") as file:
            stats = [line for line in file.readlines()]
    except FileNotFoundError:
       stats = []

    while playing:
        clear_screen()
        choice = check_menu_choice(leaderboard_menu, "Leaderboard:\n" + "\n".join([f"{index} : {leaderboard_menu[index]}" for index in range(len(leaderboard_menu))]) + "\n\n").strip().lower().replace(" ", "_")
        while choice != "back":
            leaderboard_option = 1
            leaderboards = []
            was_space = False
            for char in choice:
                if was_space:
                    choice = choice.replace(char, char.upper())
                    was_space = False
                if char == "_":
                    choice = choice.replace(char, " ")
                    was_space = True
                elif char == choice[0]:
                    choice = choice.replace(char, char.upper())
            for leaderboard_option in range(1, 3):
                leaderboard = []
                stat_option = 3 if leaderboard_option == 1 else 2
                for user in stats:
                    for game in user:
                        if game[0] == choice:
                            leaderboard.append((user[0], game[stat_option]))
                leaderboards.append(leaderboard)
            leaderboard_option = 1
            while True:
                clear_screen()
                print(f"{leaderboard_option}. {choice} Leaderboard:\n\n")
                for i, player in enumerate(leaderboards[leaderboard_option - 1]):
                    print(f"{i + 1}. {player[0]} : {player[1]}")
                print("Press enter to continue. . .")
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == "enter":
                        playing = False
                        break
                    elif event.name == "up" or event.name == "2":
                        leaderboard_option = leaderboard_option + 1 if leaderboard_option < 2 else 2
                    elif event.name == "down" or event.name == "1":
                        leaderboard_option = leaderboard_option - 1 if leaderboard_option > 1 else 1

if __name__ == "__main__":
    main()