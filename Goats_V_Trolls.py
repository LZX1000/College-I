from random import choice, shuffle
from Extras import yes_or_no, clear_screen, handle_value_error, check_menu_choice

class Player:
    def __init__(self, name, deck, is_robot=False):
        self.name = name
        self.is_robot = is_robot
        self.held_cards = []
        self.placed_cards = []
        self.discarded_cards = []
        self.resource_points = 0
        self.score = 20
        for _ in range(5):
            self.held_cards.append(choice(deck))
            deck.remove(self.held_cards[-1])

    def __str__(self):
        return self.name

def get_deck():
    deck = []
    try:
        with open ("gvtdeck.txt", "r") as file:
            for line in file:
                deck.append(line.strip())
    except FileNotFoundError:
        print("Deck file not found.")
        return None

def main(active_user='Guest'):
    clear_screen()
    deck = get_deck()
    if deck is None:
        return "Goats V Trolls", active_user, None
    main_menu = ["Quit", "Single Player", "Multiplayer"]
    playing = True
    while playing:
        # Main Menu
        while True:
            choice = check_menu_choice(main_menu, "Welcome to Goats V Trolls!\n\n" + "\n".join([f"{index} : {main_menu[index]}" for index in range(len(main_menu))]) + "\n\n").strip().lower().replace(" ", "_")
            clear_screen()
            if choice == "quit":
                playing = False
                break
            elif choice == "single_player":
                players = [Player(active_user, deck)]
                players.append(Player("Robot", deck, is_robot=True))
                break
            elif choice == "multiplayer":
                players = [Player(active_user, deck)]
                players.append(Player(input("Enter Player 2 name: ").strip(), deck))
                break
            else:
                clear_screen("Please choose a valid option.")
        for player in players:
            print(f"Player: {player.name}\n" + f"Score: {player.score}\n" + f"Resource Points: {player.resource_points}/10\n" + f"Deck: {len(deck)}\n" + f"Discarded: {len(player.discarded_cards)}\n")
            print("Battalion: " + ", ".join(player.placed_cards) + "\n")
            print("Hand: " + ", ".join(player.held_cards) + "\n")
        return "Goats V Trolls", active_user, None

if __name__ == "__main__":
    main()