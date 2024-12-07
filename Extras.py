import os
import keyboard
from typing import overload, Union, List

class Player:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f"{self.username}, {self.password}"

def clear_screen(prompt: str | None = None) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    if prompt: print(prompt)

def clear_input() -> None:
    keyboard.send('enter')
    input()

@overload
def handle_value(
    prompt: str | None = " ",
    style: Union[int, float] = 0
) -> Union[int, float]: ...

@overload
def handle_value(
    prompt: str | None = " ",
    style: str | None = " ",
    name: str | None = "string"
) -> str: ...

def handle_value(
    prompt: str | None = " ",
    style: Union[int, float, str] | None = 0,
    name: str | None = "string"
) -> Union[int, float, str]:
    while True:
        user_input = input(prompt)
        if isinstance(style, int):
            if user_input.isdigit():
                return int(user_input)
            else:
                clear_screen(f"Please enter a valid integer.\n")
        elif isinstance(style, float):
            try:
                return float(user_input)
            except ValueError:
                clear_screen(f"Please enter a valid float.\n")
        elif isinstance(style, str):
            if style == " ":
                return user_input.strip()
            elif style == "_":
                return user_input.strip().replace(" ", "_")
        clear_screen(f"Please enter a valid {name}.\n")

def yes_or_no(prompt: str | None = " ") -> str:
    while True:
        print(prompt)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name in ["n", "0"]:
                clear_input()
                return "n"
            elif event.name in ["y", "1"]:
                clear_input()
                return "y"
        clear_screen('Please enter "Y" or "N".\n')

def check_menu_choice(menu: List[str], prompt: str | None = " ") -> str:
    while True:
        print(prompt)
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            try:
                if int(event.name) in range(len(menu)):
                    clear_input()
                    return menu[int(event.name)]
            except ValueError:
                choice = input()
                if choice.strip().lower().replace(" ", "_") in [item.strip().lower().replace(" ", "_") for item in menu]:
                    return choice
        clear_screen() if event.name == "enter" else clear_screen("Invalid choice.\n")

def load_users() -> List[Player]:
    users = []
    try:
        with open("stats.txt", "r") as file:
            for line in file:
                user_info = line.strip().split("; ")
                retrieved_player = user_info[0].strip().split(", ")
                users.append(Player(retrieved_player[0], retrieved_player[1]))
    except FileNotFoundError:
        with open("stats.txt", "w") as file:
            pass
    return users

def main() -> None:
    pass

if __name__ == "__main__":
    main()