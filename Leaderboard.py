import keyboard
from typing import Tuple
from Extras import Player, multiple_choice, clear_screen

def main(active_user: Player = Player("Guest", "")) -> Tuple[str, Player, str]:
    leaderboard_menu = ["Back", "Nim", "Number Guess", "Word Guess", "The Arena", "Snake"]
    choice = " "

    try:
        with open("stats.txt", "r") as file:
            stats = [line for line in file.readlines()]
    except FileNotFoundError:
        stats = []

    while True:
        clear_screen()
        choice = multiple_choice("Leaderboard:", options=leaderboard_menu)
        if choice == "back":
            break
        
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
            stat_option = 2 if leaderboard_option == 1 else 1
            for user in stats:
                games = user.strip().split("; ")
                for game in games[1:]:
                    game_stats = game.strip().split(", ")
                    if game_stats[0] == choice:
                        leaderboard.append((games[0].split(", ")[0], game_stats[stat_option]))
            leaderboards.append(leaderboard)
        leaderboard_option = 1
        while True:
            clear_screen()
            print(f"{'a' if leaderboard_option == 1 else 'b'}.) {choice} Leaderboard:\n")
            for i, player in enumerate(leaderboards[leaderboard_option - 1]):
                print(f"{i + 1}. {player[0]} : {player[1]}")
            print("\nPress enter to continue. . .", end="")
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "enter":
                    break
                elif event.name == "down" or event.name == "2":
                    leaderboard_option = leaderboard_option + 1 if leaderboard_option < 2 else 2
                elif event.name == "up" or event.name == "1":
                    leaderboard_option = leaderboard_option - 1 if leaderboard_option > 1 else 1
    return None, active_user, None

if __name__ == "__main__":
    main()